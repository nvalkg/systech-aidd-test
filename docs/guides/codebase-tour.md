# 🗺️ Codebase Tour - Тур по кодовой базе

Подробное руководство по структуре проекта и назначению каждого файла.

---

## 📊 Карта проекта

```
systech-aidd-test/
├── 📁 src/                    # Исходный код приложения
├── 📁 tests/                  # Автоматические тесты (61 тест)
├── 📁 prompts/                # Системные промпты для специализации
├── 📁 docs/                   # Документация проекта
├── 📁 .vscode/                # Конфигурация IDE
├── 📁 .cursor/                # Правила разработки для Cursor AI
├── 📁 .github/                # CI/CD workflows
├── 📄 pyproject.toml          # Конфигурация проекта и зависимости
├── 📄 Makefile                # Команды автоматизации
├── 📄 README.md               # Главная документация
├── 📄 .env.example            # Шаблон конфигурации
└── 📄 .gitignore              # Исключения для git
```

---

## 🎯 Точки входа в приложение

### 1. `src/main.py` - Главная точка входа

**Назначение:** Инициализация и запуск всех компонентов

```python
# Что происходит при запуске:
1. Загрузка конфигурации (Config)
2. Инициализация LLMClient
3. Инициализация ConversationManager
4. Инициализация TelegramBot
5. Запуск polling
```

**Запуск:**
```bash
python src/main.py        # Прямой запуск
uv run python src/main.py # Через uv
make run                  # Через Makefile
```

### 2. `src/__main__.py` - Альтернативная точка входа

**Назначение:** Запуск как модуль

```bash
python -m src
```

**Файл просто импортирует и вызывает main() из main.py**

---

## 📦 Директория src/ - Исходный код

```
src/
├── main.py                 # Точка входа (72 строки, 97% coverage)
├── config.py               # Конфигурация (110 строк, 100% coverage)
├── telegram_bot.py         # Telegram интеграция (240 строк, 95% coverage)
├── conversation_manager.py # Оркестратор диалога (92 строки, 100% coverage)
├── llm_client.py          # OpenRouter клиент (85 строк, 96% coverage)
├── prompt_loader.py       # Загрузчик промптов (140 строк, 100% coverage)
├── history_storage.py     # Хранение истории (80 строк, 95% coverage)
├── message_formatter.py   # Форматирование для API (40 строк, 100% coverage)
├── models.py              # Модели данных (30 строк, 100% coverage)
├── __init__.py            # Python пакет
└── __main__.py            # Точка входа как модуль
```

### 📄 config.py - Конфигурация

**Класс:** `Config`

**Ответственность:**
- Загрузка переменных окружения из `.env`
- Валидация обязательных параметров (токены)
- Значения по умолчанию для опциональных параметров
- Загрузка системного промпта (из файла или переменной)

**Ключевые методы:**
```python
__init__()                    # Загрузка и валидация
_get_required_env(key)        # Получить обязательную переменную
_get_optional_env(key, default) # Получить с дефолтом
_load_system_prompt()         # Загрузить промпт (файл приоритетнее)
```

**Что хранит:**
- `telegram_token: str` - токен Telegram бота
- `openrouter_key: str` - ключ OpenRouter API
- `default_model: str` - модель LLM (по умолчанию gpt-3.5-turbo)
- `max_tokens: int` - лимит токенов ответа (1000)
- `temperature: float` - температура генерации (0.7)
- `max_history_messages: int` - размер истории (10)
- `system_prompt: str` - системный промпт

**Пример использования:**
```python
from src.config import Config

config = Config()  # Загрузит из .env
print(config.telegram_token)  # Доступ к токену
```

---

### 📄 models.py - Модели данных

**Dataclasses:** `UserMessage`, `LLMResponse`, `ConversationContext`

#### UserMessage
```python
@dataclass
class UserMessage:
    user_id: int        # ID пользователя Telegram
    text: str           # Текст сообщения
    timestamp: datetime # Время получения
```

#### LLMResponse
```python
@dataclass
class LLMResponse:
    content: str        # Ответ от LLM
    timestamp: datetime # Время генерации
    model_used: str     # Модель (напр. gpt-3.5-turbo)
```

#### ConversationContext
```python
@dataclass
class ConversationContext:
    user_id: int                    # ID пользователя
    messages: list[UserMessage]     # История сообщений
    responses: list[LLMResponse]    # История ответов
    system_prompt: str              # Системный промпт
```

**Назначение:** Структуры данных для хранения истории диалога

---

### 📄 llm_client.py - LLM клиент

**Класс:** `LLMClient`

**Ответственность:**
- Взаимодействие с OpenRouter API через openai client
- Отправка запросов к LLM
- Обработка ответов и ошибок

**Ключевые методы:**
```python
__init__(api_key, model, max_tokens, temperature)
async get_response(messages: list[dict]) -> str
```

**Как работает:**
```python
# 1. Инициализация
client = LLMClient(
    api_key="sk-or-...",
    model="openai/gpt-3.5-turbo",
    max_tokens=1000,
    temperature=0.7
)

# 2. Запрос
messages = [
    {"role": "system", "content": "You are helpful assistant"},
    {"role": "user", "content": "Hello!"}
]
response = await client.get_response(messages)
# → "Hi! How can I help you?"
```

**Обработка ошибок:**
- Логирует все ошибки API
- Пробрасывает исключения выше (обрабатывает TelegramBot)
- Обрабатывает None в content (возвращает пустую строку)

---

### 📄 prompt_loader.py - Загрузчик промптов

**Класс:** `PromptLoader`

**Ответственность:**
- Загрузка системных промптов из файлов или текста
- Парсинг структуры промпта (роль, описание)
- Форматирование информации для команды `/role`

**Ключевые методы:**
```python
__init__(prompt_text, prompt_file)  # Загрузка (файл приоритетнее)
get_system_prompt() -> str          # Полный промпт для LLM
get_role_name() -> str              # Название роли
get_role_description() -> str       # Форматированное описание
```

**Формат промпта:**
```
Роль: Python Code Reviewer Expert

Ты опытный Python разработчик...

Твои принципы:
- SOLID, DRY, KISS
- Type hints везде

Твои функции:
1. Code review
2. Рефакторинг
```

**Парсинг:**
- Ищет строку "Роль: [название]" для извлечения роли
- Остальное - описание и инструкции

---

### 📄 history_storage.py - Хранилище истории

**Класс:** `HistoryStorage`

**Ответственность:**
- Хранение контекстов диалогов в памяти
- Управление историей (добавление, обрезка)
- Очистка истории по запросу

**Структура хранения:**
```python
self.contexts: dict[int, ConversationContext]
# Ключ: user_id → Значение: ConversationContext
```

**Ключевые методы:**
```python
get_or_create_context(user_id, system_prompt) -> ConversationContext
add_message(user_id, text, system_prompt) -> None
add_response(user_id, content, model_used) -> None
get_context(user_id) -> ConversationContext | None
clear(user_id) -> None
_trim_history(user_id) -> None  # Обрезает до max_history
```

**Ограничение истории:**
- Максимум `max_history` сообщений (по умолчанию 10)
- При превышении - удаляются старые (FIFO)
- Применяется к messages и responses

---

### 📄 message_formatter.py - Форматтер сообщений

**Класс:** `MessageFormatter`

**Ответственность:**
- Преобразование ConversationContext в формат OpenAI API
- Формирование массива messages для LLM

**Ключевой метод:**
```python
@staticmethod
def format_for_llm(context: ConversationContext, system_prompt: str) -> list[dict]
```

**Что делает:**
1. Создает `system` сообщение с промптом
2. Чередует `user` и `assistant` сообщения из истории
3. Возвращает массив в формате OpenAI

**Пример вывода:**
```python
[
    {"role": "system", "content": "You are helpful assistant"},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "How are you?"}
]
```

---

### 📄 conversation_manager.py - Оркестратор диалога

**Класс:** `ConversationManager`

**Ответственность:**
- Координация компонентов (storage, formatter, llm_client)
- Обработка сообщений пользователя
- Управление flow: message → storage → format → LLM → storage

**Ключевые методы:**
```python
__init__(llm_client, system_prompt, max_history)
async process_message(user_id: int, text: str) -> str
clear_history(user_id: int) -> None
get_role_description() -> str  # Для команды /role
```

**Flow обработки:**
```python
1. storage.add_message(user_id, text)        # Сохранить сообщение
2. context = storage.get_context(user_id)    # Получить контекст
3. messages = formatter.format_for_llm(...)  # Форматировать
4. response = await llm_client.get_response(...) # Запросить LLM
5. storage.add_response(user_id, response)   # Сохранить ответ
6. return response                           # Вернуть
```

**Интеграция компонентов:**
```python
self.storage = HistoryStorage(max_history)
self.formatter = MessageFormatter()
self.llm_client = llm_client
self.prompt_loader = PromptLoader(system_prompt, None)
```

---

### 📄 telegram_bot.py - Telegram интеграция

**Класс:** `TelegramBot`

**Ответственность:**
- Обработка Telegram Bot API через aiogram 3.x
- Регистрация обработчиков команд и сообщений
- Валидация входящих данных
- Обработка ошибок с понятными сообщениями пользователю

**Команды:**
```python
/start  → cmd_start()   # Приветствие
/help   → cmd_help()    # Справка
/role   → cmd_role()    # Показать роль бота
/clear  → cmd_clear()   # Очистить историю
[текст] → handle_message() # Диалог
```

**Ключевые методы:**
```python
__init__(token, conversation_manager)
async cmd_start(message: Message) -> None
async cmd_help(message: Message) -> None
async cmd_role(message: Message) -> None
async cmd_clear(message: Message) -> None
async handle_message(message: Message) -> None
async start_polling() -> None
async stop() -> None
```

**Валидация:**
- Пустые сообщения игнорируются
- Сообщения >4000 символов отклоняются
- Проверка наличия `message.from_user`

**Обработка ошибок:**
- Try/catch в `handle_message()`
- Понятные сообщения пользователю
- Детальное логирование

**Константы:**
```python
WELCOME_TEXT = "👋 Привет! Я LLM-ассистент..."
HELP_TEXT = "ℹ️ Справка по использованию..."
ERROR_MESSAGE_GENERAL = "❌ Извините, произошла ошибка..."
ERROR_MESSAGE_TOO_LONG = "⚠️ Сообщение слишком длинное..."
MAX_MESSAGE_LENGTH = 4000
```

---

## 🧪 Директория tests/ - Тесты

```
tests/
├── conftest.py                  # Общие фикстуры pytest
├── test_config.py              # 11 тестов (Config)
├── test_models.py              # Dataclasses
├── test_llm_client.py          # 6 тестов (LLMClient)
├── test_prompt_loader.py       # 9 тестов (PromptLoader)
├── test_history_storage.py     # 6 тестов (HistoryStorage)
├── test_message_formatter.py   # 3 теста (MessageFormatter)
├── test_conversation_manager.py # 5 тестов (ConversationManager)
├── test_telegram_bot.py        # 15 тестов (TelegramBot)
└── test_main.py                # 6 тестов (main flow)
```

**Всего:** 61 тест, 96% coverage

### conftest.py - Общие фикстуры

**Фикстуры:**
```python
@pytest.fixture
def clean_env(monkeypatch)  # Очистить env переменные

@pytest.fixture
def valid_env(monkeypatch)  # Установить валидные env

@pytest.fixture
def llm_client() -> LLMClient  # Тестовый LLMClient

@pytest.fixture
def mock_llm_client()  # Мок LLMClient для тестов
```

**Использование:**
```python
def test_something(valid_env):
    config = Config()  # Будет использовать valid_env
    assert config.telegram_token == "test_telegram_token"
```

---

## 📝 Директория prompts/ - Системные промпты

```
prompts/
├── README.md                              # Документация
├── system_prompt.txt                     # Базовый ассистент
├── system_prompt_python_code_reviewer.txt # Code reviewer
└── system_prompt_technical_writer.txt     # Technical writer
```

**Формат файла:**
```
Роль: [Название]

[Описание и инструкции]
```

**Использование:**
```bash
# В .env
SYSTEM_PROMPT_FILE=prompts/system_prompt_python_code_reviewer.txt
```

---

## 📚 Директория docs/ - Документация

```
docs/
├── guides/                   # Руководства
│   ├── getting-started.md        # Быстрый старт
│   ├── codebase-tour.md         # Тур по коду (этот файл)
│   ├── architecture-overview.md # Архитектура
│   ├── visual-guide.md          # Визуальный гайд
│   └── troubleshooting.md       # Решение проблем
├── README.md                # Индекс документации
├── vision.md                # Техническое видение
├── tasklist.md              # План разработки
└── idea.md                  # Идея проекта
```

---

## ⚙️ Конфигурационные файлы

### pyproject.toml - Конфигурация проекта

**Секции:**
```toml
[project]                  # Метаданные (имя, версия, зависимости)
[project.optional-dependencies] # Dev зависимости
[tool.ruff]               # Настройки линтера/форматтера
[tool.ruff.lint]          # Правила линтинга
[tool.mypy]               # Настройки type checker
```

**Основные зависимости:**
- `aiogram>=3.0.0` - Telegram Bot API
- `openai>=1.0.0` - OpenRouter клиент
- `python-dotenv>=1.0.0` - Загрузка .env

**Dev зависимости:**
- `ruff>=0.1.0` - Форматтер + линтер
- `mypy>=1.0.0` - Type checker
- `pytest>=7.0.0` - Тестирование
- `pytest-asyncio>=0.21.0` - Async тесты
- `pytest-cov>=4.0.0` - Coverage

---

### Makefile - Автоматизация команд

```makefile
install     # uv sync - установка зависимостей
run         # python src/main.py - запуск бота
dev         # uv run python src/main.py - запуск через uv
clean       # Очистка __pycache__
format      # ruff format - форматирование
lint        # ruff check - линтинг
typecheck   # mypy - проверка типов
test        # pytest - запуск тестов
quality     # format + lint + typecheck + test
```

**Использование:**
```bash
make install   # Установить зависимости
make quality   # Проверить качество кода (обязательно перед PR!)
```

---

## 🔄 Flow обработки сообщения

```mermaid
sequenceDiagram
    participant User as 👤 User (Telegram)
    participant TB as TelegramBot
    participant CM as ConversationManager
    participant HS as HistoryStorage
    participant MF as MessageFormatter
    participant LLM as LLMClient
    participant API as OpenRouter API

    User->>TB: Отправляет сообщение
    TB->>TB: Валидация (length, empty)
    TB->>CM: process_message(user_id, text)
    CM->>HS: add_message(user_id, text)
    HS->>HS: Обрезка истории (max 10)
    CM->>HS: get_context(user_id)
    HS-->>CM: ConversationContext
    CM->>MF: format_for_llm(context)
    MF-->>CM: messages[]
    CM->>LLM: get_response(messages)
    LLM->>API: POST /chat/completions
    API-->>LLM: response
    LLM-->>CM: response_text
    CM->>HS: add_response(user_id, response)
    CM-->>TB: response_text
    TB->>User: Отправляет ответ

    style User fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style API fill:#2196F3,stroke:#0D47A1,stroke-width:2px,color:#fff
    style TB fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style CM fill:#9C27B0,stroke:#4A148C,stroke-width:2px,color:#fff
```

---

## 🧭 Путь чтения кода (рекомендуемый порядок)

### Для понимания архитектуры:

1. **`src/models.py`** ← Начни отсюда (модели данных)
2. **`src/config.py`** ← Как загружается конфигурация
3. **`src/llm_client.py`** ← Как работает LLM API
4. **`src/history_storage.py`** ← Как хранится история
5. **`src/message_formatter.py`** ← Как форматируются сообщения
6. **`src/conversation_manager.py`** ← Как все связано
7. **`src/telegram_bot.py`** ← Как обрабатываются команды
8. **`src/main.py`** ← Как все инициализируется

### Для добавления фичи:

1. Определи что хочешь добавить
2. Пройди соответствующий тест в `tests/`
3. Посмотри реализацию в `src/`
4. Добавь свой код следуя SOLID
5. Добавь тесты

### Для дебага проблемы:

1. Посмотри логи в терминале
2. Найди соответствующий модуль
3. Добавь `logger.debug(...)` для детализации
4. Запусти `make run` и проверь

---

## 📏 Метрики проекта

| Метрика | Значение |
|---------|----------|
| **Строк кода (src/)** | ~900 |
| **Модулей** | 9 |
| **Классов** | 9 (1 класс = 1 файл) |
| **Тестов** | 61 |
| **Coverage** | 96% |
| **Cyclomatic complexity** | <10 везде |

---

## 🎯 Принципы организации кода

### 1 класс = 1 файл
Каждый класс в отдельном файле с понятным именем.

### SOLID
- **SRP:** Каждый класс одна ответственность
- **OCP:** Легко расширяется (например, новые промпты)
- **LSP:** Не используется (нет наследования)
- **ISP:** Минимальные интерфейсы
- **DIP:** Зависимости через конструктор

### DRY
- Константы для текстов
- Фикстуры для тестов
- Переиспользуемые методы

### KISS
- Простые методы
- Понятные имена
- Минимум абстракций

---

## 🔍 Где что искать

| Что ищешь | Где смотреть |
|-----------|--------------|
| Конфигурация | `src/config.py` |
| Модели данных | `src/models.py` |
| API интеграция | `src/llm_client.py` |
| Telegram команды | `src/telegram_bot.py` |
| Обработка диалога | `src/conversation_manager.py` |
| Хранение истории | `src/history_storage.py` |
| Форматирование | `src/message_formatter.py` |
| Системные промпты | `prompts/` |
| Тесты | `tests/test_*.py` |
| Документация | `docs/`, `README.md` |
| Правила кодирования | `.cursor/rules/conventions.mdc` |

---

## 🎓 Следующие шаги

После изучения структуры:

1. **Запусти проект** → [getting-started.md](getting-started.md)
2. **Изучи архитектуру** → [architecture-overview.md](architecture-overview.md)
3. **Запусти тесты** → `make test`
4. **Внеси изменения** → [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Вопросы по структуре?** Смотри [troubleshooting.md](troubleshooting.md)
