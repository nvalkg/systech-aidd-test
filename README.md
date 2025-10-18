# LLM-ассистент (Telegram Bot)

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI Status](https://img.shields.io/badge/CI-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Простой и эффективный Telegram-бот с интеграцией LLM для ведения диалогов

## 📋 Описание

Telegram-бот на основе LLM (Large Language Model) для ведения контекстуальных диалогов с пользователями. Бот запоминает историю сообщений, поддерживает контекст беседы и предоставляет удобные команды для управления.

## ✨ Возможности

- 💬 **Диалог с LLM** через Telegram интерфейс
- 🧠 **Сохранение контекста** до 10 последних сообщений
- 💾 **Персистентное хранение** истории диалогов в PostgreSQL
- ⚡ **Асинхронная обработка** для быстрых ответов
- 🛡️ **Валидация сообщений** и обработка ошибок
- 📝 **Простые команды** для управления ботом
- 🔒 **Безопасное логирование** без токенов и личных данных
- 🔄 **Миграции БД** через Alembic

## 🛠️ Технологии

- **Python 3.11+** - основной язык
- **aiogram 3.x** - фреймворк для Telegram Bot API
- **OpenRouter API** - доступ к различным LLM
- **PostgreSQL** - база данных для хранения истории диалогов
- **SQLAlchemy + asyncpg** - асинхронная работа с БД
- **Alembic** - миграции схемы базы данных
- **Docker Compose** - локальное развертывание PostgreSQL
- **uv** - управление зависимостями и виртуальным окружением
- **python-dotenv** - управление конфигурацией

## 🚀 Быстрый старт

### 🐳 Quick Start с Docker (рекомендуется)

Запустите весь проект одной командой за 2 минуты:

```bash
# 1. Настройте переменные окружения
cp .env.example .env
# Отредактируйте .env: добавьте TELEGRAM_BOT_TOKEN и OPENROUTER_API_KEY

# 2. Запустите все сервисы
cd devops
docker-compose up
```

**Готово!** 🎉 Все 4 сервиса запущены и работают.

#### Доступ к сервисам

| Сервис | URL | Описание |
|--------|-----|----------|
| 🌐 **Frontend** | http://localhost:3000 | Веб-интерфейс с дашбордом и чатом |
| 🔌 **API** | http://localhost:8000 | REST API для статистики |
| 📚 **API Docs** | http://localhost:8000/docs | Swagger документация |
| 💬 **Bot** | Telegram | Найдите @your_bot_name в Telegram |
| 🗄️ **PostgreSQL** | localhost:5433 | База данных |

#### Основные команды

```bash
docker-compose up         # Запуск
docker-compose up -d      # Запуск в фоне
docker-compose ps         # Статус сервисов
docker-compose logs -f    # Просмотр логов
docker-compose down       # Остановка
```

📖 **Подробная инструкция:** [Docker Quickstart Guide](devops/doc/guides/docker-quickstart.md)
📊 **DevOps Roadmap:** [devops/doc/devops-roadmap.md](devops/doc/devops-roadmap.md)

---

### Запуск для разработки (без Docker)

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd systech-aidd-test
```

### 2. Настройка IDE (VSCode/Cursor)

Проект включает готовые конфигурации для VSCode/Cursor IDE:

```bash
# При первом открытии проекта:
# 1. IDE предложит установить рекомендованные расширения - соглашайтесь
# 2. Выберите Python интерпретатор: .venv/Scripts/python.exe
# 3. Готово! Теперь доступны:
#    - Запуск и отладка через F5 (Run & Debug)
#    - Автоформатирование при сохранении (Ctrl+S)
#    - Запуск тестов через Test Explorer
#    - Задачи через Ctrl+Shift+B
```

**Подробная документация:** [.vscode/README.md](.vscode/README.md)

### 3. Установка зависимостей

Требуется установленный [uv](https://github.com/astral-sh/uv):

```bash
# Установка зависимостей и создание виртуального окружения
make install

# Или напрямую через uv
uv sync
```

### 4. Настройка конфигурации

```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование .env файла
# Добавьте свои токены:
# - TELEGRAM_BOT_TOKEN (получить у @BotFather)
# - OPENROUTER_API_KEY (получить на openrouter.ai)
# - DATABASE_URL (по умолчанию настроен для Docker Compose)
```

### 5. Настройка базы данных

Бот использует PostgreSQL для сохранения истории диалогов между перезапусками.

#### Запуск PostgreSQL через Docker Compose (рекомендуется)

```bash
# Запуск PostgreSQL контейнера
make db-up

# Применение миграций
make db-migrate

# Проверка статуса
docker-compose ps
```

#### Команды для работы с БД

```bash
make db-up      # Запустить PostgreSQL
make db-down    # Остановить PostgreSQL
make db-migrate # Применить миграции
make db-reset   # Пересоздать БД с нуля (удалит все данные!)
make db-revision name="описание изменений"  # Создать новую миграцию
```

#### Настройка без Docker (опционально)

Если у вас уже есть PostgreSQL, измените `DATABASE_URL` в `.env`:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
```

### 6. Запуск бота

#### Через VSCode/Cursor IDE (рекомендуется)

```bash
# Способ 1: Run & Debug (F5)
1. Откройте панель Run and Debug (Ctrl+Shift+D)
2. Выберите "▶️ Run Bot"
3. Нажмите F5 или кнопку Start Debugging

# Способ 2: Задачи (Ctrl+Shift+B)
1. Нажмите Ctrl+Shift+P
2. Выберите "Tasks: Run Task"
3. Выберите "▶️ Run Bot"
```

#### Через терминал

```bash
# Запуск через make
make run

# Или через uv (с активацией окружения)
make dev

# Или напрямую
uv run python src/main.py
```

## ⚙️ Конфигурация

Все настройки задаются в файле `.env`:

### Обязательные параметры

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Необязательные параметры (со значениями по умолчанию)

```bash
# Модель LLM
DEFAULT_MODEL=openai/gpt-3.5-turbo

# Параметры генерации
MAX_TOKENS=1000              # Максимум токенов в ответе
TEMPERATURE=0.7              # Температура генерации (0.0 - 1.0)

# Управление диалогом
MAX_HISTORY_MESSAGES=10      # Максимум сообщений в истории

# Системный промпт (выберите один из вариантов)
SYSTEM_PROMPT=You are a helpful AI assistant.  # Текст промпта напрямую
# SYSTEM_PROMPT_FILE=prompts/system_prompt.txt  # 🆕 Загрузка из файла (имеет приоритет!)

# Логирование
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

### 🎭 Специализация бота (NEW!)

Бот поддерживает загрузку системных промптов из файлов для специализации:

```bash
# В .env файле укажите путь к файлу промпта:
SYSTEM_PROMPT_FILE=prompts/system_prompt_python_code_reviewer.txt
```

**Доступные специализации:**

| Промпт | Файл | Описание |
|--------|------|----------|
| 🤖 AI Assistant (default) | `prompts/system_prompt.txt` | Универсальный помощник |
| 🐍 Python Code Reviewer | `prompts/system_prompt_python_code_reviewer.txt` | Эксперт по ревью Python кода |
| 📝 Technical Writer | `prompts/system_prompt_technical_writer.txt` | Технический писатель |

**Переключение роли:**
1. Измените `SYSTEM_PROMPT_FILE` в `.env`
2. Перезапустите бота
3. Используйте `/role` для проверки текущей роли

**Создание своего промпта:**
```bash
# Создайте файл с промптом в формате:
Роль: Название Роли

Описание роли и инструкции...

Твои принципы:
- Принцип 1
- Принцип 2
```

## 🎮 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и описание возможностей |
| `/help` | Подробная справка по использованию |
| `/role` | 🆕 Показать текущую роль и специализацию бота |
| `/clear` | Очистка истории диалога |

## 📂 Структура проекта

```
systech-aidd-test/
├── src/
│   ├── main.py                 # Точка входа приложения
│   ├── config.py               # Конфигурация из .env
│   ├── llm_client.py          # Клиент для OpenRouter API
│   ├── prompt_loader.py       # 🆕 Загрузчик системных промптов
│   ├── conversation_manager.py # Управление контекстом диалога
│   ├── telegram_bot.py        # Telegram бот (aiogram)
│   ├── history_storage.py     # Хранение истории диалога
│   ├── message_formatter.py   # Форматирование сообщений для LLM
│   └── models.py              # Модели данных (dataclasses)
├── prompts/                    # 🆕 Системные промпты для специализации
│   ├── README.md              # Документация по промптам
│   ├── system_prompt.txt      # Базовый универсальный ассистент
│   ├── system_prompt_python_code_reviewer.txt  # Python Code Reviewer
│   └── system_prompt_technical_writer.txt      # Technical Writer
├── tests/                      # Автоматические тесты (61 тест, 96% coverage)
│   ├── conftest.py            # Общие фикстуры pytest
│   ├── test_config.py         # Тесты конфигурации
│   ├── test_prompt_loader.py  # 🆕 Тесты загрузчика промптов
│   ├── test_conversation_manager.py
│   ├── test_telegram_bot.py
│   └── test_*.py              # Тесты для каждого модуля
├── docs/
│   ├── roadmap.md             # Дорожная карта проекта (спринты)
│   ├── vision.md              # Техническое видение проекта
│   └── tasklists/             # Детальные планы спринтов
├── .cursor/
│   └── rules/
│       ├── conventions.mdc    # Правила разработки кода
│       ├── qa_conventions.mdc # 🆕 Правила тестирования (TDD)
│       └── workflow_tdd.mdc   # 🆕 TDD workflow
├── .vscode/                   # Конфигурация VSCode/Cursor
│   ├── launch.json            # Конфигурации запуска и отладки
│   ├── tasks.json             # Задачи для разработки
│   ├── settings.json          # Настройки проекта
│   ├── extensions.json        # Рекомендованные расширения
│   └── README.md              # Документация по IDE
├── .env.example               # Пример конфигурации
├── .gitignore                 # Исключения для git
├── pyproject.toml             # Зависимости проекта
├── Makefile                   # Автоматизация задач
└── README.md                  # Этот файл
```

## 🏗️ Архитектура

Проект следует принципу **KISS** (Keep It Simple, Stupid) и строгому **ООП** (1 класс = 1 файл):

```
┌─────────────────┐
│  TelegramBot    │  ← Обработка сообщений от пользователей
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│  ConversationManager    │  ← Управление контекстом диалога
└────────┬────────────────┘
         │
         ↓
┌─────────────────┐
│   LLMClient     │  ← Взаимодействие с OpenRouter API
└─────────────────┘
```

### Компоненты

- **Config** - загрузка и валидация конфигурации (поддержка файлов промптов)
- **PromptLoader** - 🆕 загрузка и парсинг системных промптов из файлов
- **LLMClient** - асинхронный клиент для LLM API
- **ConversationManager** - управление историей и контекстом (интеграция с PromptLoader)
- **TelegramBot** - обработка команд и сообщений (команда `/role`)
- **HistoryStorage** - хранение истории диалога в памяти
- **MessageFormatter** - форматирование сообщений для LLM API
- **main.py** - инициализация и запуск

## 🔧 Команды Makefile

```bash
make install  # Установка зависимостей через uv
make run      # Запуск бота (python src/main.py)
make dev      # Запуск с использованием uv run
make clean    # Очистка __pycache__ и .pyc файлов
```

## 📝 Разработка

### Принципы

- **KISS** - максимальная простота, никакого оверинжиниринга
- **1 класс = 1 файл** - строгое следование ООП
- **SOLID** - Single Responsibility Principle
- **DRY** - Don't Repeat Yourself
- **Async/await** - для всех операций ввода-вывода
- **Type hints** - для всех публичных методов

### Workflow разработки

Подробное руководство: [CONTRIBUTING.md](CONTRIBUTING.md)

```bash
# 1. Создание ветки
git checkout -b feature/my-feature

# 2. Разработка + тесты
# ... ваш код ...

# 3. Проверка качества (обязательно!)
make quality

# 4. Коммит и push
git commit -m "feat: описание изменений"
git push origin feature/my-feature
```

### Команды качества кода

```bash
make format     # Автоформатирование (ruff format)
make lint       # Проверка линтером (ruff check)
make typecheck  # Проверка типов (mypy)
make test       # Тесты + coverage
make quality    # Все проверки разом (обязательно перед PR!)
```

## 🧪 Тестирование

### Автоматические тесты

#### Через VSCode/Cursor IDE (рекомендуется)

```bash
# Способ 1: Test Explorer
1. Откройте панель Testing (значок колбы в левой панели)
2. Нажмите "Run All Tests" или выберите конкретный тест
3. Просмотрите результаты и coverage

# Способ 2: Debug тестов (F5)
1. Откройте файл с тестом
2. Поставьте breakpoint (F9)
3. Run & Debug → "🧪 Debug Current Test File"
4. Отлаживайте пошагово (F10, F11)

# Способ 3: Задачи (Ctrl+Shift+B)
1. Ctrl+Shift+P → "Tasks: Run Task"
2. Выберите "🧪 Run All Tests"
```

#### Через терминал

```bash
# Запуск всех тестов с coverage
make test

# Запуск конкретного модуля
uv run pytest tests/test_config.py -v

# HTML отчет coverage
uv run pytest --cov=src --cov-report=html
# Откройте htmlcov/index.html в браузере
```

### Метрики качества

| Инструмент | Цель | Текущий статус |
|-----------|------|----------------|
| Ruff (lint) | 0 ошибок | ✅ All checks passed |
| Mypy (types) | 100% coverage | ✅ Success: no issues |
| Pytest | Все passed | ✅ 61/61 passed (+19 новых) |
| Coverage | >80% | ✅ 96% |

### Структура тестов

```
tests/
├── conftest.py                  # Общие фикстуры
├── test_config.py              # Тесты конфигурации (11 тестов)
├── test_prompt_loader.py       # 🆕 Тесты загрузчика промптов (9 тестов)
├── test_conversation_manager.py # Тесты менеджера диалога (5 тестов)
├── test_telegram_bot.py        # Тесты Telegram бота (15 тестов)
├── test_history_storage.py    # Тесты хранения истории (6 тестов)
├── test_message_formatter.py  # Тесты форматирования (3 теста)
├── test_llm_client.py          # Тесты LLM клиента (6 тестов)
└── test_main.py                # Тесты точки входа (6 тестов)
```

### Coverage по модулям

| Модуль | Coverage | Статус |
|--------|----------|--------|
| config.py | 100% | ✅ |
| models.py | 100% | ✅ |
| message_formatter.py | 100% | ✅ |
| conversation_manager.py | 100% | ✅ |
| prompt_loader.py | 🆕 100% | ✅ |
| main.py | 97% | ✅ |
| llm_client.py | 96% | ✅ |
| history_storage.py | 95% | ✅ |
| telegram_bot.py | 95% | ✅ |
| **Overall** | **96%** (+1%) | ✅ |

### Ручное тестирование бота

1. Запустите бота: `make run`
2. Найдите бота в Telegram (имя из @BotFather)
3. Проверьте команды: `/start`, `/help`, `/role`, `/clear`
4. Протестируйте специализацию:
   - Измените `SYSTEM_PROMPT_FILE` в `.env`
   - Перезапустите бота
   - Проверьте `/role` - должна измениться роль
5. Отправьте несколько сообщений для проверки контекста
6. Проверьте обработку длинных и пустых сообщений

## 🔄 CI/CD

### Автоматические проверки

При каждом push и PR автоматически запускаются:

- ✅ Format check (ruff format --check)
- ✅ Lint check (ruff check)
- ✅ Type check (mypy)
- ✅ Tests + coverage (pytest)

**Конфигурация:** [.github/workflows/quality.yml](.github/workflows/quality.yml)

### Требования к PR

- ✅ Все проверки CI/CD passed
- ✅ Coverage не упал (<95%)
- ✅ Type hints для всех публичных методов
- ✅ Тесты для нового функционала
- ✅ Документация обновлена (если нужно)

## ⚠️ Ограничения MVP

- Хранение данных **только в памяти** (нет БД)
- История **теряется** при перезапуске
- Поддержка **только текстовых** сообщений
- Один диалог на пользователя (без множественных сессий)
- Максимум **10 сообщений** в истории
- Максимум **4000 символов** в сообщении

## 🐛 Решение проблем

### Бот не запускается

```bash
# Проверьте наличие токенов в .env
cat .env

# Проверьте логи при запуске
make run
```

### Ошибка "Token is invalid"

- Убедитесь, что `TELEGRAM_BOT_TOKEN` корректен
- Получите новый токен у @BotFather если нужно

### Ошибка при запросе к LLM

- Проверьте `OPENROUTER_API_KEY`
- Убедитесь, что модель доступна (по умолчанию: `openai/gpt-3.5-turbo`)
- Проверьте баланс на openrouter.ai

### Бот не отвечает

- Используйте `/clear` для очистки истории
- Перезапустите бота
- Проверьте логи на наличие ошибок

## 💻 Разработка в IDE

### VSCode/Cursor конфигурация

Проект включает полную настройку для комфортной разработки:

- **Автоматическое форматирование** при сохранении (Ruff)
- **Интеграция линтера** (ошибки в Problems panel)
- **Type checking** (MyPy интеграция)
- **Test Explorer** для визуального запуска тестов
- **Готовые конфигурации запуска** (F5)
- **Задачи для всех команд** (Ctrl+Shift+B)

**Полная документация:** [.vscode/README.md](.vscode/README.md)

### Горячие клавиши

| Действие | Клавиша |
|----------|---------|
| Запуск/Отладка бота | `F5` |
| Поставить breakpoint | `F9` |
| Запустить задачу | `Ctrl+Shift+B` |
| Форматировать код | `Alt+Shift+F` |
| Показать Problems | `Ctrl+Shift+M` |
| Открыть терминал | `` Ctrl+` `` |

## 📚 Полезные ссылки

- [Документация aiogram](https://docs.aiogram.dev/)
- [OpenRouter API](https://openrouter.ai/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [uv documentation](https://github.com/astral-sh/uv)
- **[VSCode/Cursor Setup](.vscode/README.md)** - Настройка IDE

## 📄 Лицензия

MIT License

## 👥 Автор

Разработано как MVP для проверки концепции LLM-ассистента в Telegram.

---

**Статус:** ✅ MVP готов к использованию
**Версия:** 1.0.0
**Последнее обновление:** 2025-10-11
