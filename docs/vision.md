# Vision - Техническое видение проекта LLM-ассистента

## Технологии

### Основные технологии
- **Python 3.11+** - основной язык разработки
- **uv** - быстрый менеджер зависимостей (замена pip/poetry)
- **aiogram 3.x** - современная асинхронная библиотека для Telegram Bot API с поддержкой polling
- **openai** - официальный клиент для работы с LLM через OpenRouter
- **python-dotenv** - загрузка переменных окружения
- **make** - автоматизация сборки и запуска

### Обоснование выбора
- **uv** - в 10-100 раз быстрее pip, простая настройка
- **aiogram** - самая популярная и стабильная библиотека для Telegram ботов в Python
- **polling** - проще webhook'ов для MVP, не требует публичного URL
- **OpenRouter** - единый API для доступа к разным LLM моделям

### Структура зависимостей
```
pyproject.toml - конфигурация проекта и зависимости
requirements.txt - для совместимости
Makefile - команды сборки
.env.example - шаблон переменных окружения
```

## Качество кода

### Инструменты

#### Ruff - форматтер и линтер
- **Замена:** black + isort + flake8 + pyupgrade
- **Скорость:** написан на Rust, очень быстрый
- **Конфигурация:** pyproject.toml
- **Правила:** PEP 8, pyflakes, bugbear, mccabe
- **Line length:** 100 символов

#### Mypy - статический анализатор типов
- **Проверка:** type hints во всех публичных методах
- **Режим:** strict mode (disallow_untyped_defs)
- **Цель:** 100% type coverage

#### Pytest - тестирование
- **Framework:** pytest с плагинами
- **Async:** pytest-asyncio для async тестов
- **Coverage:** pytest-cov, цель >80%
- **Моки:** unittest.mock для зависимостей

### Команды Make

```bash
make format      # Автоформатирование кода (ruff format)
make lint        # Проверка линтером (ruff check)
make typecheck   # Проверка типов (mypy)
make test        # Запуск тестов (pytest + coverage)
make quality     # Все проверки разом
```

### Метрики качества

| Метрика | Цель |
|---------|------|
| Ruff errors | 0 |
| Mypy type coverage | 100% |
| Test coverage | >80% |
| Cyclomatic complexity | <10 |

### Workflow

1. **Разработка:** пишем код
2. **Форматирование:** `make format`
3. **Проверка:** `make quality`
4. **Коммит:** только при успешном `make quality`

## Тестирование

### Подход к тестированию

#### Unit тесты
- **Цель:** покрытие >80%
- **Фреймворк:** pytest + pytest-asyncio + pytest-cov
- **Изоляция:** unittest.mock для зависимостей
- **Фикстуры:** conftest.py для переиспользования

#### Структура тестов
```
tests/
├── conftest.py              # Общие фикстуры
├── test_config.py           # Config (100% coverage) ✅
├── test_llm_client.py       # LLMClient
├── test_conversation_manager.py  # ConversationManager
├── test_telegram_bot.py     # TelegramBot
└── test_integration.py      # Интеграционные тесты
```

### Принципы

#### Arrange-Act-Assert
```python
def test_something():
    # Arrange: подготовка
    config = Config()

    # Act: действие
    result = config.do_something()

    # Assert: проверка
    assert result == expected_value
```

#### Изоляция тестов
- Каждый тест независим
- Используем фикстуры для чистого состояния
- Моки для внешних зависимостей (load_dotenv, API)
- monkeypatch для переменных окружения

#### Понятные имена
- `test_config_missing_token` - ясно, что тестируется
- `test_llm_client_api_error` - сценарий описан в имени
- Используем docstring для описания теста

### Фикстуры

#### clean_env
Очищает все переменные окружения для изолированных тестов.

#### valid_env
Устанавливает минимальный набор валидных переменных окружения.

### Примеры тестов

#### Тест на успешный сценарий
```python
def test_config_valid(valid_env):
    """Тест: Config успешно загружается"""
    config = Config()
    assert config.telegram_token == "test_telegram_token"
```

#### Тест на ошибку
```python
def test_config_invalid_max_tokens(valid_env, monkeypatch):
    """Тест: ValueError при невалидном MAX_TOKENS"""
    monkeypatch.setenv("MAX_TOKENS", "not_a_number")

    with pytest.raises(ValueError, match="MAX_TOKENS должно быть целым числом"):
        Config()
```

### Тестирование async кода

#### Async тесты с pytest-asyncio
```python
@pytest.mark.asyncio
async def test_get_response_success(llm_client: LLMClient) -> None:
    """Тест успешного получения ответа от LLM"""
    # Arrange: Подготовка mock ответа
    mock_response = Mock(
        choices=[Mock(message=Mock(content="Test response"))],
        usage=Mock(total_tokens=50)
    )

    # Act: Мокирование async вызова
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response
        result = await llm_client.get_response([{"role": "user", "content": "Hi"}])

        # Assert
        assert result == "Test response"
        mock_create.assert_called_once()
```

#### Мокирование внешних API
- **AsyncMock** для async методов
- **patch.object** для точечной подмены
- **side_effect** для симуляции ошибок

```python
@pytest.mark.asyncio
async def test_get_response_api_error(llm_client: LLMClient) -> None:
    """Тест обработки ошибки API"""
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            await llm_client.get_response([{"role": "user", "content": "Hi"}])
```

### Coverage метрики

#### Достигнутые показатели (после итерации 5)
| Модуль | Coverage | Статус |
|--------|----------|--------|
| config.py | 100% | ✅ Excellent |
| models.py | 100% | ✅ Excellent |
| message_formatter.py | 100% | ✅ Excellent |
| conversation_manager.py | 100% | ✅ Excellent |
| llm_client.py | 96% | ✅ Excellent |
| main.py | 97% | ✅ Excellent |
| history_storage.py | 95% | ✅ Excellent |
| telegram_bot.py | 94% | ✅ Excellent |
| **TOTAL** | **95%** | ✅ **Excellent** |

#### Целевые метрики
- **Общий coverage:** >80% ✅ **Достигнуто: 95%**
- **Критичные модули:** 100% (config, models) ✅
- **Бизнес-логика:** >90% (llm_client, conversation_manager) ✅
- **Интеграция:** >80% (telegram_bot, main) ✅

#### Команды для работы с coverage
```bash
# Обычный запуск с coverage
make test

# Детальный HTML отчет
pytest --cov=src --cov-report=html
# Открыть htmlcov/index.html в браузере

# Coverage для конкретного модуля
pytest tests/test_llm_client.py --cov=src.llm_client --cov-report=term-missing
```

### TDD практики (Test-Driven Development)

#### Цикл Red-Green-Refactor

1. **🔴 Red** - Пишем failing тест
   ```python
   def test_get_response_handles_none():
       """LLM может вернуть None - нужно обработать"""
       # Тест падает - код не готов
   ```

2. **🟢 Green** - Минимальная реализация
   ```python
   if content is None:
       content = ""
   # Тест проходит
   ```

3. **🔵 Refactor** - Улучшаем код
   ```python
   # Применяем SOLID, DRY
   # Тесты остаются зелеными
   ```

#### Преимущества TDD
- ✅ Тесты документируют поведение
- ✅ Высокий coverage (95% в нашем случае)
- ✅ Меньше регрессий при изменениях
- ✅ Дизайн кода улучшается

## Качество и надежность

### Стратегия тестирования

#### Многоуровневое тестирование
1. **Unit тесты** - изолированное тестирование классов
   - Мокируем все внешние зависимости
   - Один тест = один сценарий
   - Coverage >95% для критичного кода

2. **Integration тесты** - взаимодействие компонентов
   - Проверяем flow: message → ConversationManager → LLMClient
   - Мокируем только внешние API (AsyncOpenAI)
   - Проверяем корректность данных между компонентами

3. **Manual тесты** - ручное тестирование бота
   - Проверка UX в реальном Telegram
   - Тестирование граничных случаев
   - Валидация ответов LLM

#### Типы тестов в проекте
- ✅ **Config тесты** - валидация конфигурации (11 тестов, 100% coverage) - обновлено
- ✅ **PromptLoader тесты** - 🆕 загрузка и парсинг промптов (9 тестов, 100% coverage)
- ✅ **LLMClient тесты** - работа с API (6 тестов, 96% coverage)
- ✅ **ConversationManager тесты** - управление диалогом (5 тестов, 100% coverage) - обновлено
- ✅ **HistoryStorage тесты** - хранение истории (6 тестов, 95% coverage)
- ✅ **MessageFormatter тесты** - форматирование (3 теста, 100% coverage)
- ✅ **TelegramBot тесты** - обработка команд (15 тестов, 95% coverage) - обновлено
- ✅ **Main тесты** - интеграция компонентов (6 тестов, 97% coverage)

**Всего: 61 тест (+19 новых), 96% coverage (+1%)**

### Обработка ошибок

#### Fail Fast принцип
- **Валидация на старте** - проверка токенов при инициализации Config
- **Понятные сообщения** - ValueError с описанием проблемы
- **Логирование** - все ошибки логируются с деталями

#### Обработка API ошибок
```python
try:
    response = await self.client.chat.completions.create(...)
    content = response.choices[0].message.content
    if content is None:  # Обработка None
        content = ""
    return content
except Exception as e:
    logger.error(f"Ошибка при запросе к LLM: {e}")
    raise  # Пробрасываем выше
```

#### Уровни обработки
1. **LLMClient** - ловит API ошибки, логирует, пробрасывает
2. **ConversationManager** - пробрасывает дальше
3. **TelegramBot** - показывает пользователю понятное сообщение
4. **Main** - обрабатывает критичные ошибки (config, startup)

### Надежность

#### Type Safety
- **100% type hints** для всех публичных методов
- **Mypy strict mode** - disallow_untyped_defs = true
- **Type checking** в CI/CD pipeline

#### Code Quality
- **Ruff lint** - 0 ошибок, 0 предупреждений
- **Cyclomatic complexity** <10 для всех методов
- **DRY принцип** - нет дублирования кода
- **SOLID принципы** - Single Responsibility для всех классов

#### Автоматизация проверок
```bash
make quality  # format + lint + typecheck + test
```

Все проверки должны проходить перед коммитом:
- ✅ Ruff format - код отформатирован
- ✅ Ruff lint - 0 ошибок
- ✅ Mypy - 0 type errors
- ✅ Pytest - 42/42 тесты passed
- ✅ Coverage - 95% (цель >80%)

## Принцип разработки

### Основные принципы
- **KISS (Keep It Simple, Stupid)** - максимальная простота, никакого оверинжиниринга
- **ООП с жестким соблюдением правила "1 класс = 1 файл"**
- **Минимализм** - только необходимый функционал для проверки идеи
- **Асинхронность** - использование async/await для эффективной работы с API

### Структура классов
Каждый класс в отдельном файле с четкой ответственностью:

1. **`TelegramBot`** (`telegram_bot.py`) - только работа с Telegram API, команда `/role`
2. **`LLMClient`** (`llm_client.py`) - только взаимодействие с OpenRouter
3. **`ConversationManager`** (`conversation_manager.py`) - только управление диалогом, интеграция компонентов
4. **`PromptLoader`** (`prompt_loader.py`) - 🆕 загрузка и парсинг системных промптов
5. **`HistoryStorage`** (`history_storage.py`) - хранение истории диалога в памяти
6. **`MessageFormatter`** (`message_formatter.py`) - форматирование сообщений для LLM
7. **`Config`** (`config.py`) - только загрузка конфигурации, поддержка файлов промптов

### Принципы кодирования
- Один класс = одна ответственность
- Минимум зависимостей между классами
- Простые методы без сложной логики
- Прямолинейный код без абстракций
- Обработка ошибок на верхнем уровне

### Структура файлов
```
src/
├── telegram_bot.py
├── llm_client.py
├── conversation_manager.py
├── config.py
└── main.py
```

## Структура проекта

### Минимальная файловая структура
```
telegram-llm-bot/
├── src/
│   ├── __init__.py          # Python пакет
│   ├── __main__.py          # Точка входа для python -m src
│   ├── models.py            # Модели данных (SRP)
│   ├── history_storage.py   # Хранилище истории (SRP)
│   ├── message_formatter.py # Форматирование для API (SRP)
│   ├── conversation_manager.py  # Оркестратор диалога (SRP)
│   ├── telegram_bot.py      # TelegramBot класс
│   ├── llm_client.py        # LLMClient класс
│   ├── config.py            # Config класс
│   └── main.py              # Точка входа
├── prompts/
│   ├── README.md            # Документация по промптам
│   ├── system_prompt.txt    # Базовый системный промпт
│   ├── system_prompt_python_code_reviewer.txt  # Специализация: Code Reviewer
│   └── system_prompt_technical_writer.txt      # Специализация: Technical Writer
├── tests/
│   ├── conftest.py          # Фикстуры pytest
│   ├── test_config.py       # Тесты конфигурации
│   ├── test_history_storage.py     # Тесты хранилища
│   ├── test_message_formatter.py   # Тесты форматтера
│   └── test_conversation_manager.py # Тесты менеджера
├── pyproject.toml           # Конфигурация проекта и зависимости
├── Makefile                 # Команды сборки и проверки
├── .env.example             # Шаблон переменных окружения
├── .env                     # Локальные настройки (в .gitignore)
├── .gitignore
└── README.md
```

### Описание файлов
- **`src/`** - весь исходный код
- **`prompts/`** - системные промпты для специализированных ролей
- **`tests/`** - unit и integration тесты
- **`pyproject.toml`** - конфигурация uv, зависимости, метаданные
- **`Makefile`** - простые команды: `make install`, `make run`, `make dev`
- **`.env.example`** - шаблон с необходимыми переменными
- **`.env`** - реальные настройки (не коммитится)

### Команды Makefile
```makefile
install:     # uv sync
run:         # python src/main.py
dev:         # uv run python src/main.py
clean:       # очистка кэша
```

## Архитектура проекта

### Основные компоненты и их взаимодействие

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   TelegramBot   │───▶│ConversationManager│───▶│   LLMClient     │
│                 │    │                  │    │                 │
│ - Получение     │    │ - Управление     │    │ - Запросы к     │
│   сообщений     │    │   диалогом       │    │   OpenRouter    │
│ - Отправка      │    │ - Формирование   │    │ - Обработка     │
│   ответов       │    │   промптов       │    │   ответов       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │     Config       │
                    │                  │
                    │ - Токены         │
                    │ - Настройки      │
                    └──────────────────┘
```

### Поток данных
1. **TelegramBot** получает сообщение от пользователя
2. **ConversationManager** добавляет сообщение в контекст диалога
3. **ConversationManager** формирует промпт для LLM
4. **LLMClient** отправляет запрос в OpenRouter
5. **LLMClient** возвращает ответ от LLM
6. **ConversationManager** обновляет контекст диалога
7. **TelegramBot** отправляет ответ пользователю

### Зависимости между классами
- **TelegramBot** → **ConversationManager** → **LLMClient**
- **Все классы** → **Config**
- Никаких циклических зависимостей

### Принципы взаимодействия
- Слабая связанность - классы знают только о том, что им нужно
- Простые интерфейсы - минимум методов
- Прямолинейный поток данных
- Обработка ошибок на уровне main.py

### Архитектура диалога (SOLID)

После рефакторинга в соответствии с **Single Responsibility Principle (SRP)**, `ConversationManager` разделен на специализированные компоненты:

```
ConversationManager (Orchestrator)
├── PromptLoader          # 🆕 Загрузка и парсинг промптов
│   ├── _load_prompt()        # Загрузка из файла/текста
│   ├── _parse_role_name()    # Извлечение роли
│   ├── get_system_prompt()   # Полный промпт для LLM
│   ├── get_role_name()       # Название роли
│   └── get_role_description() # Описание для команды /role
├── HistoryStorage        # Хранение истории
│   ├── get_or_create_context()
│   ├── add_message()
│   ├── add_response()
│   ├── get_context()
│   ├── clear()
│   └── _trim_history()
├── MessageFormatter      # Форматирование для API
│   └── format_for_llm()
└── LLMClient            # Взаимодействие с API
    └── get_response()
```

**Преимущества архитектуры:**
- ✅ **Модульность**: каждый компонент отвечает за одну задачу
- ✅ **Тестируемость**: компоненты легко тестируются изолированно
- ✅ **Гибкость**: легко заменить способ хранения или форматирования
- ✅ **Читаемость**: код сократился с 142 до 92 строк

**Компоненты:**

1. **models.py** - модели данных (UserMessage, LLMResponse, ConversationContext)
2. **history_storage.py** - хранение и управление историей диалогов
3. **message_formatter.py** - форматирование контекста для LLM API
4. **conversation_manager.py** - оркестратор, координирующий компоненты
5. **prompt_loader.py** (v1.1, планируется) - загрузка системных промптов из файлов

## Модель данных

### Простые структуры данных для MVP

#### 1. Сообщение пользователя
```python
# В models.py
@dataclass
class UserMessage:
    user_id: int
    text: str
    timestamp: datetime
```

#### 2. Ответ LLM
```python
# В models.py
@dataclass
class LLMResponse:
    content: str
    timestamp: datetime
    model_used: str
```

#### 3. Контекст диалога
```python
# В models.py
@dataclass
class ConversationContext:
    user_id: int
    messages: list[UserMessage]
    responses: list[LLMResponse]
    system_prompt: str
```

### Принципы хранения данных
- **В памяти** - для MVP не нужна база данных
- **Один диалог на пользователя** - простейшая реализация
- **Ограничение истории** - максимум 10 последних сообщений для экономии токенов
- **Автоочистка** - старые диалоги удаляются при перезапуске

### Структура данных
```
ConversationContext
├── user_id: int
├── system_prompt: str
├── messages: [UserMessage1, UserMessage2, ...]
└── responses: [LLMResponse1, LLMResponse2, ...]
```

### Ограничения для MVP
- Максимум 10 сообщений в истории диалога
- Только текстовые сообщения (без файлов, фото, стикеров)
- Один активный диалог на пользователя
- Нет персистентности - данные теряются при перезапуске

## Работа с LLM

### Интеграция через OpenRouter

#### Основные параметры
- **Провайдер**: OpenRouter API
- **Клиент**: официальная библиотека `openai`
- **Модель по умолчанию**: `openai/gpt-3.5-turbo` (баланс цена/качество)
- **Метод**: `chat.completions.create()`

#### Структура запроса
```python
# В llm_client.py
{
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "system_prompt"},
        {"role": "user", "content": "user_message_1"},
        {"role": "assistant", "content": "assistant_response_1"},
        {"role": "user", "content": "current_message"}
    ],
    "max_tokens": 1000,
    "temperature": 0.7
}
```

#### Обработка ответа
- Извлечение `content` из `choices[0].message.content`
- Простая обработка ошибок (retry, fallback)
- Логирование запросов и ответов

#### Конфигурация
```python
# В config.py
OPENROUTER_API_KEY = "your_key"
DEFAULT_MODEL = "openai/gpt-3.5-turbo"
MAX_TOKENS = 1000
TEMPERATURE = 0.7
```

### Принципы работы
- **Простота** - минимум настроек, максимум по умолчанию
- **Надежность** - обработка ошибок сети и API
- **Экономия** - ограничение токенов и истории
- **Прозрачность** - логирование для отладки

## Сценарии работы

### Основной сценарий (Happy Path)
1. **Запуск бота** - `python src/main.py`
2. **Пользователь отправляет `/start`** - бот приветствует и объясняет возможности
3. **Пользователь пишет сообщение** - бот обрабатывает и отвечает через LLM
4. **Диалог продолжается** - контекст сохраняется в памяти
5. **Перезапуск бота** - контекст теряется, диалог начинается заново

### Дополнительные сценарии

#### Обработка ошибок
- **Ошибка LLM API** - бот отвечает "Извините, произошла ошибка. Попробуйте позже"
- **Пустое сообщение** - бот игнорирует
- **Слишком длинное сообщение** - бот отвечает "Сообщение слишком длинное"

#### Команды бота
- **`/start`** - приветствие и инструкции
- **`/help`** - справка по командам
- **`/role`** - отображение роли и возможностей бота (v1.1)
- **`/clear`** - очистка истории диалога
- **Любое другое сообщение** - отправка в LLM

### Пользовательский опыт
- **Простота** - никаких сложных команд
- **Отзывчивость** - быстрые ответы (в пределах API)
- **Понятность** - четкие сообщения об ошибках
- **Интуитивность** - работает как обычный чат

### Ограничения MVP
- Только текстовые сообщения
- Один диалог на пользователя
- Нет сохранения между перезапусками
- Фиксированная роль (задается через .env или файл промпта)

### Специализация роли (v1.1+)

#### Концепция
Проект эволюционирует от универсального ассистента к **специализированному AI-продукту**:
- Не "помощник для всего", а эксперт в конкретной области
- Четко определенная роль через системный промпт
- Оптимизация промпта для специфичных задач

#### Команда `/role`
Отображает текущую роль и возможности бота:
```
🎭 Моя роль: Python Code Reviewer Expert

📋 Описание:
Опытный Python разработчик, специализирующийся на code review

✨ Я могу помочь вам:
• Ревью кода с рекомендациями
• Рефакторинг с объяснениями
• Поиск багов и проблем
• Советы по SOLID, DRY, KISS

💡 Пример использования:
"Ревью этого кода: [ваш код]"

⚙️ Модель: openai/gpt-3.5-turbo
```

#### Примеры специализаций
- **Python Code Reviewer** - ревью кода, рефакторинг, best practices
- **Technical Writer** - API документация, README, tutorials
- **DevOps Consultant** - CI/CD, Docker, Kubernetes
- **Security Auditor** - анализ безопасности кода

### Обработка ошибок

#### Стратегия обработки

**Принцип: Fail Gracefully**
- Пользователь всегда получает понятное сообщение об ошибке
- Ошибки логируются для отладки
- Бот продолжает работать после ошибки

#### Типы ошибок

**1. Валидация входных данных**
```python
# Пустые сообщения игнорируются
if not text or not text.strip():
    logger.info(f"Игнорируем пустое сообщение от user {user_id}")
    return

# Слишком длинные сообщения отклоняются
if len(text) > MAX_MESSAGE_LENGTH:
    error_text = ERROR_MESSAGE_TOO_LONG.format(
        length=len(text), max_length=MAX_MESSAGE_LENGTH
    )
    await message.answer(error_text)
    return
```

**2. Ошибки конфигурации**
```python
# Config.py валидирует при инициализации
def _get_required_env(self, key: str) -> str:
    value = os.getenv(key, "")
    if not value:
        raise ValueError(f"{key} не установлен в .env файле")
    return value
```

**3. Ошибки LLM API**
```python
# В handle_message()
try:
    response = await self.conversation_manager.process_message(user_id, text)
    await message.answer(response)
except Exception as e:
    logger.error(f"Ошибка при обработке сообщения от user {user_id}: {e}")
    await message.answer(ERROR_MESSAGE_GENERAL)
```

**4. Безопасная работа с данными пользователя**
```python
def _get_user_info(self, message: Message) -> tuple[int, str]:
    """Безопасное извлечение информации о пользователе"""
    if not message.from_user:
        raise ValueError("Message has no user information")

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Unknown"
    return user_id, username
```

#### Текстовые константы для ошибок

Все сообщения об ошибках вынесены в константы:
```python
ERROR_MESSAGE_TOO_LONG = """⚠️ Сообщение слишком длинное ({length} символов).
Максимальная длина: {max_length} символов.

Пожалуйста, сократи сообщение и попробуй снова."""

ERROR_MESSAGE_GENERAL = """❌ Извините, произошла ошибка при обработке вашего сообщения.

Попробуйте:
• Переформулировать вопрос
• Использовать /clear для очистки истории
• Повторить попытку позже"""
```

#### Логирование

**Уровни логирования:**
- `INFO` - штатные операции (получение сообщения, отправка ответа)
- `WARNING` - отклонение длинных сообщений
- `ERROR` - исключения при обработке

**Примеры:**
```python
logger.info(f"Получено сообщение от user {user_id}: {len(text)} символов")
logger.warning(f"Слишком длинное сообщение от user {user_id}: {len(text)} символов")
logger.error(f"Ошибка при обработке сообщения от user {user_id}: {e}")
```

## Подход к конфигурированию

### Простая конфигурация через .env

#### Структура .env файла
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# OpenRouter API
OPENROUTER_API_KEY=your_openrouter_api_key

# LLM Settings
DEFAULT_MODEL=openai/gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7

# Bot Settings
MAX_HISTORY_MESSAGES=10

# System Prompt (выбери один из способов)
# Способ 1: Прямое указание
SYSTEM_PROMPT=You are a helpful AI assistant.

# Способ 2: Загрузка из файла (v1.1, планируется)
# SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
# SYSTEM_PROMPT_FILE=prompts/system_prompt_python_code_reviewer.txt

# Logging
LOG_LEVEL=INFO
```

#### Загрузка конфигурации
```python
# В config.py
class Config:
    def __init__(self):
        load_dotenv()
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.default_model = os.getenv('DEFAULT_MODEL', 'openai/gpt-3.5-turbo')
        # ... остальные параметры
```

### Принципы конфигурации
- **Все в .env** - никаких config файлов
- **Значения по умолчанию** - для необязательных параметров
- **Валидация при запуске** - проверка обязательных токенов
- **Простота** - минимум настроек, максимум работает "из коробки"

### Файлы конфигурации
- **`.env`** - реальные настройки (в .gitignore)
- **`.env.example`** - шаблон для разработчиков
- **`config.py`** - класс для загрузки и валидации

### Валидация
- Проверка наличия обязательных токенов при запуске
- Простые сообщения об ошибках
- Остановка бота при отсутствии критических настроек

## Подход к логгированию

### Простое консольное логирование

#### Настройка логирования
```python
# В main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

#### Уровни логирования
- **INFO** - основная информация (запуск, получение сообщений, ответы)
- **ERROR** - ошибки (проблемы с API, исключения)
- **DEBUG** - детальная отладка (только при разработке)

#### Что логируем
- **Запуск/остановка бота**
- **Получение сообщений от пользователей** (user_id, текст)
- **Запросы к LLM** (модель, количество токенов)
- **Ответы от LLM** (время обработки, длина ответа)
- **Ошибки** (тип ошибки, детали)

#### Структура логов
```
2024-01-15 10:30:15 - TelegramBot - INFO - Bot started
2024-01-15 10:30:20 - TelegramBot - INFO - Received message from user 123: "Привет"
2024-01-15 10:30:21 - LLMClient - INFO - Sent request to openai/gpt-3.5-turbo
2024-01-15 10:30:22 - LLMClient - INFO - Received response (150 tokens, 1.2s)
2024-01-15 10:30:22 - TelegramBot - INFO - Sent response to user 123
```

### Принципы логирования
- **Простота** - только консоль, никаких файлов
- **Информативность** - достаточно для отладки
- **Производительность** - минимум влияния на скорость
- **Безопасность** - не логируем токены и личные данные

### Конфигурация через .env
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## Работа с системными промптами

### Концепция специализации

Вместо универсального ассистента создаются **AI-продукты с конкретными ролями**.

### Хранение промптов

**Директория:** `prompts/`

**Структура файла промпта:**
```
Роль: [Название роли]

[Описание - кто ты и чем занимаешься]

Твои принципы:
- [Принцип 1]
- [Принцип 2]

Твои функции:
1. [Функция 1]
2. [Функция 2]

Формат ответа:
- [Структура ответа]

Ограничения:
- [Что НЕ делаешь]
```

### Загрузка промпта (v1.1+)

**Через переменную окружения:**
```bash
# .env
SYSTEM_PROMPT_FILE=prompts/system_prompt_python_code_reviewer.txt
```

**PromptLoader класс (планируется):**
```python
class PromptLoader:
    def __init__(self, prompt_file: str | None = None):
        self.prompt = self._load_prompt(prompt_file)
        self.role_info = self._parse_role_info()

    def get_role_description(self) -> str:
        """Форматирование для команды /role"""
        return self._format_role_description(self.role_info)
```

### Примеры специализаций

**Python Code Reviewer:**
- Ревью кода с SOLID, DRY, KISS
- Type hints и mypy
- Рефакторинг и best practices

**Technical Writer:**
- API документация
- README и tutorials
- Архитектурная документация

**DevOps Consultant:**
- CI/CD pipeline советы
- Docker и Kubernetes
- Infrastructure as Code

---

## 🔄 CI/CD Pipeline

### Автоматизация проверок качества

**GitHub Actions** обеспечивает автоматическую проверку качества кода при каждом push и Pull Request.

#### Конфигурация

**Файл:** `.github/workflows/quality.yml`

**Триггеры:**
```yaml
on:
  push:
    branches: [ main, develop, day03-refactor ]
  pull_request:
    branches: [ main, develop ]
```

**Этапы проверки:**
```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      1. Checkout code
      2. Install uv (package manager)
      3. Set up Python 3.11
      4. Install dependencies: uv sync --dev
      5. Format check: ruff format src/ --check
      6. Lint: ruff check src/
      7. Typecheck: mypy src/
      8. Tests + coverage: pytest --cov=src --cov-report=xml
      9. Upload coverage (optional)
```

#### Преимущества CI/CD

**Для разработчиков:**
- ✅ Автоматическая проверка качества перед merge
- ✅ Раннее обнаружение ошибок (до code review)
- ✅ Единый стандарт для всей команды
- ✅ Меньше времени на ручные проверки

**Для проекта:**
- ✅ Стабильность main ветки
- ✅ Предотвращение merge кода с ошибками
- ✅ Контроль coverage (не даем ему упасть)
- ✅ Документированные требования качества

**Для code review:**
- ✅ Reviewer видит статус CI сразу в PR
- ✅ Фокус на архитектуре, не на синтаксисе
- ✅ Автоматическая проверка стандартов кодирования

#### Workflow разработчика

```bash
# 1. Создание feature-ветки
git checkout -b feature/new-functionality

# 2. Разработка + тесты
# ... код ...

# 3. Локальная проверка (ОБЯЗАТЕЛЬНО!)
make quality  # format + lint + typecheck + test

# 4. Коммит и push
git commit -m "feat: новая функциональность"
git push origin feature/new-functionality

# 5. Создание PR
# CI автоматически запустится и проверит код

# 6. Code review после успешного CI
# Merge в main только при passing CI + approved review
```

#### Метрики в README

Badges для визуализации статуса проекта:

```markdown
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI Status](https://img.shields.io/badge/CI-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

#### Требования к Pull Request

**Автоматические проверки (CI):**
- ✅ Format check passed (ruff format)
- ✅ Lint check passed (ruff check, 0 ошибок)
- ✅ Type check passed (mypy, 100% type hints)
- ✅ Tests passed (pytest, 42/42 passed)
- ✅ Coverage >= 95%

**Ручная проверка (Code Review):**
- ✅ Соблюдение SOLID (особенно SRP)
- ✅ Отсутствие дублирования (DRY)
- ✅ Понятные имена и структура
- ✅ Документация обновлена (если нужно)

#### Интеграция с Codecov (опционально)

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: false
```

По умолчанию отключено (`if: false`). Включается при наличии Codecov токена.

### Документация для разработчиков

**CONTRIBUTING.md** - полное руководство по участию в проекте:
- Процесс разработки (fork, branch, PR)
- Требования к коду (SOLID, DRY, type hints)
- Написание тестов (pytest, AsyncMock)
- Локальные проверки (`make quality`)
- Работа с CI/CD
- Решение проблем при failed CI

---

**Документ создан:** 2024-01-15
**Версия:** 3.0
**Обновлено:** 2025-10-11
**Изменения в v3.0:**
- Концепция специализированных AI-продуктов
- Команда `/role` для отображения возможностей
- Системные промпты в директории `prompts/`
- PromptLoader для загрузки промптов из файлов (v1.1)
- Примеры специализаций (Python Code Reviewer, Technical Writer)

**Статус:** v1.0 MVP готов + CI/CD настроен → v1.1 планируется (команда /role)
