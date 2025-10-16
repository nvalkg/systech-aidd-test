# Tasklist: SPRINT-1 - Persistent Storage

> **Статус:** ✅ Completed (2025-10-16)
> **Цель:** Реализовать персистентное хранение истории диалогов в PostgreSQL

---

## 📋 Обзор спринта

**Основная задача:** Заменить in-memory хранилище (`HistoryStorage`) на персистентное хранение в PostgreSQL с использованием SQLAlchemy Core и Alembic для миграций.

**Принципы:**
- KISS - максимальная простота решения
- Async/await - полная асинхронность
- Repository pattern - слой доступа к данным
- Soft delete - данные помечаются как удаленные, не удаляются физически
- Test coverage - сохранение 95%+ покрытия тестами

---

## 🎯 Критерии успеха

- [x] История диалогов сохраняется между перезапусками бота
- [x] Test coverage остается >= 95%
- [x] Все новые компоненты покрыты тестами
- [x] Документация актуализирована (README, ADR, vision, idea, roadmap)
- [x] Ручное тестирование персистентности пройдено успешно

---

## 📝 Задачи спринта

### 1. Подготовка и проектирование

#### 1.1. Анализ требований
- [x] Изучить текущую реализацию `HistoryStorage`
- [x] Определить операции с данными (CRUD)
- [x] Определить требования к soft delete
- [x] Спроектировать интерфейс Repository

**Результат:** Понимание требований, интерфейс Repository

#### 1.2. Выбор технологий
- [x] Сравнить SQLite vs PostgreSQL vs MongoDB
- [x] Выбрать инструмент миграций (Alembic)
- [x] Документировать решение в ADR-001
- [x] Согласовать с пользователем выбор PostgreSQL

**Результат:** [ADR-001: Database and Migrations](../adr/001-database-and-migrations.md)

#### 1.3. Проектирование схемы БД
- [x] Спроектировать таблицу `conversations`
- [x] Спроектировать таблицу `user_messages`
- [x] Спроектировать таблицу `llm_responses`
- [x] Определить связи (Foreign Keys)
- [x] Спроектировать индексы для производительности
- [x] Добавить поля для soft delete (is_deleted)
- [x] Добавить timestamps (created_at, updated_at)

**Результат:** Схема БД готова (3 таблицы, связи, индексы)

---

### 2. Настройка инфраструктуры

#### 2.1. Настройка PostgreSQL через Docker
- [x] Создать `docker-compose.yml`
  - PostgreSQL 16 alpine
  - Порт 5433 (избежание конфликта с локальным PostgreSQL)
  - Пользователь, пароль, БД: aidd
  - Volume для персистентности данных
  - Healthcheck для мониторинга
- [x] Добавить команды в Makefile:
  - `make db-up` - запуск PostgreSQL
  - `make db-down` - остановка PostgreSQL
  - `make db-reset` - полный сброс БД
- [x] Обновить `.gitignore` (data/, *.db, *.db-journal)

**Результат:** Docker Compose настроен, Makefile команды работают

#### 2.2. Обновление зависимостей
- [x] Добавить `asyncpg>=0.29.0` в `pyproject.toml`
- [x] Обновить `.env.example` с `DATABASE_URL`
- [x] Добавить `DATABASE_URL` в `Config`
- [x] Запустить `uv sync` для установки зависимостей

**Результат:** Все зависимости установлены, конфигурация готова

#### 2.3. Настройка Alembic
- [x] Инициализировать Alembic: `uv run alembic init alembic`
- [x] Настроить `alembic.ini` (убрать hardcoded URL)
- [x] Обновить `alembic/env.py`:
  - Импорт Config и metadata
  - Загрузка DATABASE_URL из конфигурации
  - Поддержка async миграций
- [x] Добавить команды в Makefile:
  - `make db-migrate` - применить миграции
  - `make db-revision` - создать миграцию

**Результат:** Alembic настроен для async миграций

---

### 3. Реализация слоя данных

#### 3.1. Создание схемы БД (src/database.py)
- [x] Определить `metadata` для SQLAlchemy Core
- [x] Создать таблицу `conversations`:
  - id (PK, autoincrement)
  - user_id (BigInteger, index) - исправлено с Integer
  - system_prompt (Text)
  - created_at, updated_at (DateTime)
- [x] Создать таблицу `user_messages`:
  - id (PK, autoincrement)
  - conversation_id (FK, cascade delete, index)
  - user_id (BigInteger, index)
  - text (Text)
  - content_length (Integer)
  - timestamp (DateTime)
  - is_deleted (Boolean, default False, index)
- [x] Создать таблицу `llm_responses`:
  - id (PK, autoincrement)
  - conversation_id (FK, cascade delete, index)
  - content (Text)
  - content_length (Integer)
  - model_used (String)
  - timestamp (DateTime)
  - is_deleted (Boolean, default False, index)
- [x] Создать функцию `create_engine()` для AsyncEngine

**Результат:** `src/database.py` с полной схемой БД

#### 3.2. Создание начальной миграции
- [x] Создать миграцию: `make db-revision name="initial schema"`
- [x] Проверить сгенерированную миграцию
- [x] Применить миграцию: `make db-migrate`
- [x] Проверить схему в PostgreSQL

**Результат:** Миграция `0f132edeb3b2_initial_schema` создана и применена

#### 3.3. Реализация DatabaseHistoryStorage
- [x] Создать `src/db_history_storage.py`
- [x] Реализовать `__init__(engine, max_history)`
- [x] Реализовать async `get_or_create_context(user_id, system_prompt)`:
  - Поиск существующего conversation
  - Создание нового при отсутствии
  - Загрузка messages и responses (только is_deleted=False)
  - Возврат ConversationContext
- [x] Реализовать async `add_message(user_id, text, system_prompt)`:
  - get_or_create_context
  - Вставка message
  - Вызов _trim_history
- [x] Реализовать async `add_response(user_id, content, model)`:
  - Получение conversation_id
  - Вставка response
  - Обновление updated_at
  - Вызов _trim_history
- [x] Реализовать async `get_context(user_id)`:
  - Поиск conversation
  - Загрузка полного контекста через get_or_create_context
- [x] Реализовать async `clear(user_id)` (soft delete):
  - Найти conversation_id
  - UPDATE is_deleted=True для всех messages
  - UPDATE is_deleted=True для всех responses
- [x] Реализовать async `_trim_history(conversation_id)` (soft delete):
  - Подсчет активных messages
  - Soft delete старых messages при превышении max_history
  - Аналогично для responses

**Результат:** `DatabaseHistoryStorage` с полной реализацией Repository pattern

---

### 4. Интеграция в приложение

#### 4.1. Обновление ConversationManager
- [x] Добавить поддержку DatabaseHistoryStorage в type hints
- [x] Проверка типа storage для async/sync вызовов
- [x] Обновить `process_message()`:
  - await storage.add_message() для DatabaseHistoryStorage
  - await storage.get_context()
  - await storage.add_response()
- [x] Обновить `clear_history()`:
  - await storage.clear()

**Результат:** ConversationManager поддерживает оба типа storage

#### 4.2. Обновление main.py
- [x] Импорт `create_engine` из `src.database`
- [x] Импорт `DatabaseHistoryStorage`
- [x] Создание AsyncEngine при запуске
- [x] Инициализация DatabaseHistoryStorage с engine
- [x] Передача в ConversationManager
- [x] Graceful shutdown: `await engine.dispose()`

**Результат:** Приложение использует PostgreSQL для истории

#### 4.3. Обновление TelegramBot
- [x] Обновить `cmd_clear()`: `await self.conversation_manager.clear_history()`

**Результат:** Команды бота работают с async storage

---

### 5. Тестирование

#### 5.1. Unit тесты для DatabaseHistoryStorage
- [x] Создать `tests/test_db_history_storage.py`
- [x] Создать фикстуру `test_db_engine` (SQLite in-memory)
- [x] Тест: инициализация DatabaseHistoryStorage
- [x] Тест: add_message сохраняет сообщение
- [x] Тест: add_response сохраняет ответ
- [x] Тест: trim_history обрезает старые сообщения (soft delete)
- [x] Тест: clear помечает все как удаленные (soft delete)
- [x] Тест: get_context возвращает None для несуществующего user
- [x] Тест: get_or_create_context создает новый контекст
- [x] Тест: поддержка нескольких пользователей

**Результат:** 8 новых тестов, все проходят

#### 5.2. Обновление существующих тестов
- [x] Обновить `tests/conftest.py`:
  - Добавить `pytest-asyncio`
  - Создать фикстуру `test_db_engine`
- [x] Обновить `tests/test_conversation_manager.py`:
  - `await clear_history()`
- [x] Обновить `tests/test_telegram_bot.py`:
  - Mock `clear_history` как AsyncMock
- [x] Обновить `tests/test_main.py`:
  - Mock `create_engine` и `DatabaseHistoryStorage`
  - Проверка `engine.dispose()` при остановке

**Результат:** Все тесты обновлены и проходят

#### 5.3. Проверка coverage
- [x] Запустить `make test`
- [x] Убедиться, что coverage >= 95%
- [x] Проверить покрытие новых файлов:
  - `src/database.py` >= 85%
  - `src/db_history_storage.py` >= 95%

**Результат:** 69 тестов, 95% coverage ✅

#### 5.4. Ручное тестирование
- [x] Запустить PostgreSQL: `make db-up`
- [x] Применить миграции: `make db-migrate`
- [x] Создать `.env` с токенами
- [x] Запустить бота: `uv run python -m src`
- [x] Тест 1: Отправить `/start` - должен ответить
- [x] Тест 2: Отправить сообщение - должен ответить через LLM
- [x] Тест 3: Проверить контекст - бот помнит предыдущие сообщения
- [x] Тест 4: Остановить бота (Ctrl+C)
- [x] Тест 5: Запустить бота снова
- [x] Тест 6: Отправить сообщение - бот должен помнить историю! ✅
- [x] Проверить данные в БД:
  ```bash
  docker exec aidd-postgres psql -U aidd -d aidd \
    -c "SELECT * FROM conversations;"
  docker exec aidd-postgres psql -U aidd -d aidd \
    -c "SELECT id, text, content_length FROM user_messages;"
  ```

**Результат:** Персистентность работает! История сохраняется между перезапусками.

---

### 6. Исправление багов

#### 6.1. Баг: user_id превышает Integer (int32)
**Проблема:** Telegram user_id = 5198055406 > 2147483647 (max int32)
```
asyncpg.exceptions.DataError: invalid input for query argument $1:
5198055406 (value out of int32 range)
```

**Решение:**
- [x] Изменить тип `user_id` с `Integer` на `BigInteger` в обеих таблицах
- [x] Создать миграцию: `make db-revision name="change user_id to bigint"`
- [x] Пересоздать БД: `make db-reset`
- [x] Применить миграции: `make db-migrate`
- [x] Проверить: `docker exec aidd-postgres psql -U aidd -d aidd -c "\d conversations"`

**Результат:** Миграция `bd7b2d0ee30e_change_user_id_to_bigint` применена ✅

---

### 7. Документация

#### 7.1. Создание ADR-001
- [x] Создать `docs/adr/001-database-and-migrations.md`
- [x] Описать контекст и требования
- [x] Сравнить варианты (SQLite vs PostgreSQL vs MongoDB)
- [x] Обосновать выбор PostgreSQL
- [x] Описать последствия и риски
- [x] Добавить метрики успеха

**Результат:** ADR-001 создан и задокументирован

#### 7.2. Обновление README.md
- [x] Добавить раздел "Настройка базы данных"
- [x] Добавить PostgreSQL, SQLAlchemy, Alembic в технологии
- [x] Добавить Docker Compose в инструкции
- [x] Добавить новые команды Makefile (db-*)
- [x] Обновить инструкции по запуску

**Результат:** README актуализирован

#### 7.3. Обновление vision.md
- [x] Добавить PostgreSQL, SQLAlchemy, Alembic в список технологий
- [x] Добавить обоснования выбора
- [x] Обновить структуру классов (DatabaseHistoryStorage)
- [x] Изменить принципы хранения: с in-memory на PostgreSQL
- [x] Убрать ограничение "нет персистентности"

**Результат:** vision.md обновлен

#### 7.4. Обновление idea.md
- [x] Изменить версию с MVP на v1.1
- [x] Добавить PostgreSQL в технический стек
- [x] Обновить список компонентов (DatabaseHistoryStorage, Database)
- [x] Отметить персистентность как реализованную
- [x] Обновить планы развития (v1.2)

**Результат:** idea.md обновлен

#### 7.5. Обновление roadmap.md
- [x] Изменить статус SPRINT-1 на "Completed"
- [x] Добавить ссылку на ADR-001
- [x] Добавить ссылку на tasklist-sprint-1.md
- [x] Обновить прогресс: 2/2 спринта (100%)
- [x] Добавить раздел "Ключевые достижения Sprint-1"

**Результат:** roadmap.md обновлен

#### 7.6. Создание tasklist-sprint-1.md
- [x] Создать этот файл с детальным планом спринта
- [x] Описать все выполненные задачи
- [x] Добавить критерии успеха
- [x] Документировать баги и решения

**Результат:** Этот файл ✅

---

## 📊 Итоговые метрики

### Код
- **Файлы добавлены:** 3
  - `src/database.py` (схема БД)
  - `src/db_history_storage.py` (Repository)
  - `tests/test_db_history_storage.py` (тесты)
- **Файлы изменены:** 10+
  - `src/main.py`, `src/config.py`, `src/conversation_manager.py`
  - `src/telegram_bot.py`, `tests/conftest.py`
  - `pyproject.toml`, `docker-compose.yml`, `alembic.ini`
  - `.env.example`, `.gitignore`, `Makefile`, `README.md`

### Миграции
- **Миграция 1:** `0f132edeb3b2_initial_schema` - создание таблиц
- **Миграция 2:** `bd7b2d0ee30e_change_user_id_to_bigint` - исправление типа

### Тесты
- **Новые тесты:** 8
- **Всего тестов:** 69
- **Coverage:** 95%
- **Длительность:** ~5 секунд

### База данных
- **Таблицы:** 3 (conversations, user_messages, llm_responses)
- **Индексы:** 6 (user_id, conversation_id, is_deleted)
- **Миграции:** 2
- **Soft delete:** ✅ реализовано

---

## 🎯 Результат спринта

✅ **SPRINT-1 завершен успешно!**

**Достигнуто:**
1. ✅ Персистентное хранение в PostgreSQL реализовано
2. ✅ История сохраняется между перезапусками (ручное тестирование пройдено)
3. ✅ Soft delete реализован для всех данных
4. ✅ Repository pattern применен (DatabaseHistoryStorage)
5. ✅ Асинхронность сохранена (async/await везде)
6. ✅ Test coverage = 95% (цель достигнута)
7. ✅ Документация полностью обновлена
8. ✅ ADR-001 создан и согласован
9. ✅ Docker Compose настроен
10. ✅ Makefile команды добавлены

**Баги исправлены:**
- ✅ BigInteger для Telegram user_id

**Качество:**
- 69 тестов passed ✅
- 95% coverage ✅
- 0 linter errors ✅
- 100% type hints ✅

---

## 📚 Связанные документы

- [ADR-001: Database and Migrations](../adr/001-database-and-migrations.md)
- [Roadmap - SPRINT-1](../roadmap.md)
- [Technical Vision](../vision.md)
- [Project Idea](../idea.md)
- [README](../../README.md)

---

**Версия:** 1.0
**Создан:** 2025-10-16
**Статус:** ✅ Completed
**Автор:** AI Assistant & User
