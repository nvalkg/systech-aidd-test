# LLM-ассистент (Telegram Bot)

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI Status](https://img.shields.io/badge/CI-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Простой и эффективный Telegram-бот с интеграцией LLM для ведения диалогов

## 📋 Описание

Telegram-бот на основе LLM (Large Language Model) для ведения контекстуальных диалогов с пользователями. Бот запоминает историю сообщений, поддерживает контекст беседы и предоставляет удобные команды для управления.

## ✨ Возможности

- 💬 **Диалог с LLM** через Telegram интерфейс
- 🧠 **Сохранение контекста** до 10 последних сообщений
- ⚡ **Асинхронная обработка** для быстрых ответов
- 🛡️ **Валидация сообщений** и обработка ошибок
- 📝 **Простые команды** для управления ботом
- 🔒 **Безопасное логирование** без токенов и личных данных

## 🛠️ Технологии

- **Python 3.11+** - основной язык
- **aiogram 3.x** - фреймворк для Telegram Bot API
- **OpenRouter API** - доступ к различным LLM
- **uv** - управление зависимостями и виртуальным окружением
- **python-dotenv** - управление конфигурацией

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd systech-aidd-test
```

### 2. Установка зависимостей

Требуется установленный [uv](https://github.com/astral-sh/uv):

```bash
# Установка зависимостей и создание виртуального окружения
make install

# Или напрямую через uv
uv sync
```

### 3. Настройка конфигурации

```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование .env файла
# Добавьте свои токены:
# - TELEGRAM_BOT_TOKEN (получить у @BotFather)
# - OPENROUTER_API_KEY (получить на openrouter.ai)
```

### 4. Запуск бота

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
SYSTEM_PROMPT=You are a helpful AI assistant.

# Логирование
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

## 🎮 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и описание возможностей |
| `/help` | Подробная справка по использованию |
| `/clear` | Очистка истории диалога |

## 📂 Структура проекта

```
systech-aidd-test/
├── src/
│   ├── main.py                 # Точка входа приложения
│   ├── config.py               # Конфигурация из .env
│   ├── llm_client.py          # Клиент для OpenRouter API
│   ├── conversation_manager.py # Управление контекстом диалога
│   └── telegram_bot.py        # Telegram бот (aiogram)
├── docs/
│   ├── vision.md              # Техническое видение проекта
│   └── tasklist.md            # План разработки
├── .cursor/
│   └── rules/
│       ├── conventions.mdc    # Правила разработки
│       └── workflow.mdc       # Процесс разработки
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

- **Config** - загрузка и валидация конфигурации
- **LLMClient** - асинхронный клиент для LLM API
- **ConversationManager** - управление историей и контекстом
- **TelegramBot** - обработка команд и сообщений
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
| Pytest | Все passed | ✅ 42/42 passed |
| Coverage | >80% | ✅ 95% |

### Структура тестов

```
tests/
├── conftest.py                  # Общие фикстуры
├── test_config.py              # Тесты конфигурации
├── test_models.py              # Тесты моделей данных
├── test_history_storage.py    # Тесты хранения истории
├── test_message_formatter.py  # Тесты форматирования
├── test_conversation_manager.py # Тесты менеджера диалога
├── test_llm_client.py          # Тесты LLM клиента
├── test_telegram_bot.py        # Тесты Telegram бота
└── test_main.py                # Тесты точки входа
```

### Coverage по модулям

| Модуль | Coverage | Статус |
|--------|----------|--------|
| config.py | 100% | ✅ |
| models.py | 100% | ✅ |
| message_formatter.py | 100% | ✅ |
| conversation_manager.py | 100% | ✅ |
| llm_client.py | 96% | ✅ |
| main.py | 97% | ✅ |
| history_storage.py | 95% | ✅ |
| telegram_bot.py | 94% | ✅ |
| **Overall** | **95%** | ✅ |

### Ручное тестирование бота

1. Запустите бота: `make run`
2. Найдите бота в Telegram (имя из @BotFather)
3. Проверьте команды: `/start`, `/help`, `/clear`
4. Отправьте несколько сообщений для проверки контекста
5. Проверьте обработку длинных и пустых сообщений

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

## 📚 Полезные ссылки

- [Документация aiogram](https://docs.aiogram.dev/)
- [OpenRouter API](https://openrouter.ai/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [uv documentation](https://github.com/astral-sh/uv)

## 📄 Лицензия

MIT License

## 👥 Автор

Разработано как MVP для проверки концепции LLM-ассистента в Telegram.

---

**Статус:** ✅ MVP готов к использованию  
**Версия:** 1.0.0  
**Последнее обновление:** 2025-10-11
