<!-- 355ff46e-edf4-464d-a22c-2d7a909ec3a5 be0effcb-2d70-4faf-bd3f-39e6a5929932 -->
# SPRINT-1: Персистентное хранилище истории диалогов

## Обзор

Заменяем in-memory хранилище (`HistoryStorage`) на персистентное хранение в PostgreSQL. Модели уже содержат необходимые поля (`timestamp`, `content_length`, `id`, `is_deleted`).

## Ключевые файлы

- `src/history_storage.py` - текущее in-memory хранилище
- `src/models.py` - модели данных (уже содержат нужные поля)
- `docs/adr/001-database-and-migrations.md` - ADR с выбором SQLite (обновим на PostgreSQL)

## Этапы реализации

### 1. Инфраструктура и конфигурация

- Обновить ADR-001 с обоснованием выбора PostgreSQL
- Создать `docker-compose.yml` с PostgreSQL (порт 5432, volume для данных)
- Добавить настройки БД в `src/config.py` (DATABASE_URL из .env)
- Обновить `.env.example` с примером DATABASE_URL
- Добавить `psycopg2-binary` в зависимости `pyproject.toml`

### 2. Настройка Alembic

- Инициализировать Alembic: `alembic init alembic`
- Настроить `alembic.ini` для работы с config.py
- Настроить `alembic/env.py` для SQLAlchemy Core и асинхронности

### 3. Схема базы данных

Создать SQLAlchemy Core схему в новом файле `src/database.py`:

- Таблица `conversations`: id, user_id, system_prompt, created_at
- Таблица `user_messages`: id, conversation_id, user_id, text, content_length, timestamp, is_deleted
- Таблица `llm_responses`: id, conversation_id, content, content_length, model_used, timestamp, is_deleted
- Индексы: user_id, conversation_id, is_deleted
- Связи: FK от messages/responses к conversations

### 4. Первая миграция

- Создать миграцию с таблицами: `alembic revision --autogenerate -m "initial schema"`
- Проверить сгенерированную миграцию

### 5. Repository для работы с БД

Создать `src/db_history_storage.py` (Repository pattern):

- Класс `DatabaseHistoryStorage` с теми же методами, что и `HistoryStorage`
- `add_message()`, `add_response()`, `get_context()`, `clear()` (soft delete)
- Использовать SQLAlchemy Core (не ORM) для простоты
- Асинхронные операции с `asyncpg` + `sqlalchemy.ext.asyncio`

### 6. Интеграция с приложением

- Обновить `src/main.py` для создания движка БД и применения миграций при старте
- Заменить `HistoryStorage` на `DatabaseHistoryStorage` в `ConversationManager`
- Добавить graceful shutdown с закрытием соединений БД

### 7. Тесты

- Обновить `tests/test_history_storage.py` для работы с БД (использовать тестовую БД или SQLite в памяти)
- Добавить фикстуры в `tests/conftest.py` для настройки тестовой БД
- Обеспечить изоляцию тестов (rollback после каждого теста)
- Поддержать 95%+ coverage

### 8. Документация

- Обновить `README.md` с инструкциями по запуску PostgreSQL
- Добавить в `Makefile` команды: `db-up`, `db-down`, `db-migrate`, `db-reset`
- Обновить `docs/guides/getting-started.md` с шагами настройки БД

## Принципы реализации

- **KISS**: минимальная функциональность, никакого оверинжиниринга
- **Soft delete**: is_deleted=True, физически не удаляем
- **Async-first**: все операции БД асинхронные
- **Тестируемость**: 95%+ coverage с изолированными тестами

### To-dos

- [ ] Настроить инфраструктуру: docker-compose.yml, config.py, зависимости
- [ ] Инициализировать и настроить Alembic для миграций
- [ ] Создать схему БД в src/database.py и первую миграцию
- [ ] Реализовать DatabaseHistoryStorage с Repository pattern
- [ ] Интегрировать DatabaseHistoryStorage в приложение
- [ ] Обновить тесты для работы с БД, обеспечить 95%+ coverage
- [ ] Обновить документацию и README с инструкциями по БД
- [ ] Обновить ADR-001 с обоснованием выбора PostgreSQL