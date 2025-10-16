# План разработки LLM-ассистента

## 📊 Отчет о прогрессе

| Итерация | Статус | Описание | Дата завершения |
|----------|--------|----------|-----------------|
| 1️⃣ Подготовка и конфигурация | ✅ Done | Инициализация проекта и настройка | 2025-10-10 |
| 2️⃣ LLM Client | ✅ Done | Интеграция с OpenRouter | 2025-10-10 |
| 3️⃣ Conversation Manager | ✅ Done | Управление диалогами | 2025-10-10 |
| 4️⃣ Telegram Bot | ✅ Done | Базовая интеграция | 2025-10-10 |
| 5️⃣ Интеграция | ✅ Done | Полная связка компонентов | 2025-10-11 |
| 6️⃣ Команды | ✅ Done | Команды бота | 2025-10-11 |
| 7️⃣ Финализация | ✅ Done | Полировка и документация | 2025-10-11 |
| 8️⃣ Команда /role и промпты | ✅ Done | Специализация через системные промпты | 2025-10-11 |

**Легенда статусов:**
- ⏳ Pending - Ожидает выполнения
- 🔄 In Progress - В работе
- ✅ Done - Завершено
- ❌ Blocked - Заблокировано

---

## 📋 Итерационный план

### Итерация 1️⃣: Подготовка проекта и конфигурация

**Цель:** Инициализация структуры проекта, зависимостей и настройка конфигурации

#### Задачи:
- [x] Создать структуру директорий `src/`
- [x] Создать `pyproject.toml` с метаданными проекта
- [x] Добавить зависимости: `aiogram`, `openai`, `python-dotenv`
- [x] Создать `Makefile` с командами `install`, `run`, `dev`, `clean`
- [x] Создать `.env.example` с шаблоном переменных
- [x] Создать `.gitignore` (`.env`, `__pycache__`, `.venv`)
- [x] Выполнить `make install` для установки зависимостей
- [x] Создать `src/config.py` с классом `Config`
- [x] Реализовать загрузку переменных через `python-dotenv`
- [x] Добавить валидацию обязательных токенов
- [x] Добавить значения по умолчанию для необязательных параметров
- [x] Создать простой `src/main.py` для тестирования загрузки конфига

**Переменные .env:**
```bash
TELEGRAM_BOT_TOKEN=test_token
OPENROUTER_API_KEY=test_key
DEFAULT_MODEL=openai/gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7
MAX_HISTORY_MESSAGES=10
SYSTEM_PROMPT=You are a helpful AI assistant.
LOG_LEVEL=INFO
```

**Тест:** `uv sync` устанавливает зависимости, `python src/main.py` загружает и выводит конфигурацию

---

### Итерация 2️⃣: LLM Client

**Цель:** Интеграция с OpenRouter через openai client

#### Задачи:
- [x] Создать `src/llm_client.py` с классом `LLMClient`
- [x] Инициализация openai client с `base_url` для OpenRouter
- [x] Реализовать async метод `get_response(messages: list) -> str`
- [x] Добавить обработку ошибок и логирование
- [x] Создать тестовый скрипт в `main.py` для проверки LLM

**Тест:** Отправить тестовый запрос в OpenRouter и получить ответ

---

### Итерация 3️⃣: Conversation Manager

**Цель:** Управление контекстом диалога

#### Задачи:
- [x] Создать `src/conversation_manager.py`
- [x] Определить dataclass-ы: `UserMessage`, `LLMResponse`, `ConversationContext`
- [x] Реализовать класс `ConversationManager`
- [x] Методы: `add_user_message()`, `add_llm_response()`, `get_messages_for_llm()`
- [x] Ограничение истории до 10 сообщений
- [x] Интегрировать с `LLMClient`
- [x] Добавить метод `clear_history()`

**Тест:** Создать диалог из нескольких сообщений и получить ответы от LLM

---

### Итерация 4️⃣: Telegram Bot (базовая версия)

**Цель:** Базовая интеграция с Telegram через aiogram

#### Задачи:
- [x] Создать `src/telegram_bot.py` с классом `TelegramBot`
- [x] Инициализация `Bot` и `Dispatcher` из aiogram
- [x] Реализовать обработчик команды `/start`
- [x] Настроить polling
- [x] Добавить логирование запуска и получения сообщений
- [x] Обновить `main.py` для запуска бота

**Тест:** Запустить бота, отправить `/start`, получить приветствие

---

### Итерация 5️⃣: Полная интеграция

**Цель:** Связать все компоненты в единую систему

#### Задачи:
- [x] Интегрировать `ConversationManager` в `TelegramBot`
- [x] Обработчик текстовых сообщений → ConversationManager → LLMClient
- [x] Отправка ответа пользователю
- [x] Хранение контекста для каждого `user_id` (dict в памяти)
- [x] Обработка ошибок с понятными сообщениями пользователю
- [x] Настройка полного логирования потока данных

**Тест:** Вести полноценный диалог сботом через Telegram

---

### Итерация 6️⃣: Команды бота

**Цель:** Добавить служебные команды

#### Задачи:
- [x] Реализовать команду `/help` - справка по использованию
- [x] Реализовать команду `/clear` - очистка истории диалога
- [x] Добавить обработку пустых сообщений
- [x] Добавить проверку на слишком длинные сообщения (>4000 символов)
- [x] Улучшить приветствие в `/start` с инструкциями

**Тест:** Проверить все команды и edge cases (пустые, длинные сообщения)

---

### Итерация 7️⃣: Финализация

**Цель:** Полировка и документация

#### Задачи:
- [x] Проверить все type hints
- [x] Добавить docstrings для всех классов
- [x] Финальная проверка логирования (без токенов/личных данных)
- [x] Создать `README.md` с инструкциями по запуску
- [x] Проверить `.env.example` на актуальность
- [x] Финальное тестирование всех сценариев
- [x] Code review по `conventions.mdc`

**Тест:** Полный цикл: установка → настройка → запуск → диалог → команды

---

### Итерация 8️⃣: Команда /role и специализированные промпты (TDD)

**Цель:** Реализовать отображение роли бота и загрузку системных промптов из файлов

**Подход:** Test-Driven Development (Red → Green → Refactor)

#### Фаза 🔴 RED: Написать failing тесты

**Задачи:**
- [ ] Создать `tests/test_prompt_loader.py`
  - [ ] `test_prompt_loader_init_with_default_prompt()` - загрузка дефолтного промпта
  - [ ] `test_prompt_loader_init_with_file()` - загрузка из файла
  - [ ] `test_prompt_loader_file_not_found()` - обработка отсутствующего файла
  - [ ] `test_prompt_loader_parse_role_info()` - парсинг информации о роли
  - [ ] `test_prompt_loader_get_role_description()` - форматирование для /role
  - [ ] `test_prompt_loader_get_system_prompt()` - получение промпта

- [ ] Обновить `tests/test_config.py`
  - [ ] `test_config_system_prompt_from_env()` - промпт из SYSTEM_PROMPT
  - [ ] `test_config_system_prompt_from_file()` - промпт из SYSTEM_PROMPT_FILE
  - [ ] `test_config_system_prompt_file_priority()` - приоритет FILE над ENV
  - [ ] `test_config_system_prompt_file_not_found()` - fallback на ENV

- [ ] Обновить `tests/test_telegram_bot.py`
  - [ ] `test_cmd_role_default_prompt()` - отображение базовой роли
  - [ ] `test_cmd_role_specialized_prompt()` - отображение специализированной роли
  - [ ] `test_cmd_role_formatting()` - проверка форматирования ответа

**Запуск тестов (должны упасть):**
```bash
pytest tests/test_prompt_loader.py -v
# → FAILED: ModuleNotFoundError: No module named 'src.prompt_loader'

pytest tests/test_config.py::test_config_system_prompt_from_file -v
# → FAILED: AttributeError: 'Config' has no attribute 'system_prompt_file'

pytest tests/test_telegram_bot.py::test_cmd_role_default_prompt -v
# → FAILED: AttributeError: 'TelegramBot' has no attribute 'cmd_role'
```

**Критерий готовности RED:** Все тесты написаны и падают с понятными ошибками

---

#### Фаза 🟢 GREEN: Минимальная реализация

**Задачи:**
- [ ] Создать `src/prompt_loader.py` с классом `PromptLoader`
  - [ ] `__init__(prompt_text: str | None, prompt_file: str | None)` - инициализация
  - [ ] `_load_prompt_from_file(file_path: str) -> str` - загрузка из файла
  - [ ] `_parse_role_info() -> dict` - парсинг структуры промпта
  - [ ] `get_role_description() -> str` - форматирование для команды /role
  - [ ] `get_system_prompt() -> str` - получение промпта для LLM

- [ ] Обновить `src/config.py`
  - [ ] Добавить поле `system_prompt_file: str | None`
  - [ ] Добавить метод `_load_system_prompt() -> str`
  - [ ] Логика приоритета: SYSTEM_PROMPT_FILE → SYSTEM_PROMPT → default

- [ ] Обновить `src/telegram_bot.py`
  - [ ] Добавить константу `ROLE_TEXT_FORMAT` для форматирования
  - [ ] Реализовать `async def cmd_role(self, message: Message) -> None`
  - [ ] Зарегистрировать обработчик команды `/role`

- [ ] Обновить `src/conversation_manager.py`
  - [ ] Добавить метод `get_role_description() -> str`
  - [ ] Передавать PromptLoader в ConversationManager

**Запуск тестов (должны пройти):**
```bash
make test
# → 50+ tests passed (было 42)
# → Coverage: ~95%
```

**Критерий готовности GREEN:** Все тесты проходят, coverage не упал

---

#### Фаза 🔵 REFACTOR: Улучшение кода

**Задачи:**
- [ ] Рефакторинг `PromptLoader`
  - [ ] Применить SRP: разделить загрузку и парсинг
  - [ ] Добавить валидацию формата промпта
  - [ ] Улучшить обработку ошибок (FileNotFoundError → понятное сообщение)

- [ ] Рефакторинг `Config`
  - [ ] Вынести константы (DEFAULT_PROMPT, PROMPT_DIR)
  - [ ] Добавить type hints для всех новых методов
  - [ ] Docstrings для новых методов

- [ ] Рефакторинг `TelegramBot`
  - [ ] DRY: вынести форматирование в отдельный метод
  - [ ] Константы для текстов ответов
  - [ ] Улучшить читаемость `cmd_role()`

- [ ] Проверка качества
  - [ ] `make format` - автоформатирование
  - [ ] `make lint` - исправить все замечания (0 ошибок)
  - [ ] `make typecheck` - проверить типы (0 ошибок)
  - [ ] `make test` - все тесты passed
  - [ ] `make quality` - финальная проверка

**Запуск проверок:**
```bash
make quality
# → Format: ✓
# → Lint: ✓ (0 errors)
# → Typecheck: ✓ (Success: no issues found)
# → Tests: 50/50 passed
# → Coverage: 95%
```

**Критерий готовности REFACTOR:** Код чистый, тесты зеленые, качество отличное

---

#### Интеграция и документация

**Задачи:**
- [ ] Обновить `README.md`
  - [ ] Добавить раздел "Специализация бота"
  - [ ] Инструкция по использованию промптов из файлов
  - [ ] Примеры использования команды `/role`

- [ ] Обновить `.env.example`
  - [ ] Добавить `SYSTEM_PROMPT_FILE` с примерами

- [ ] Обновить `docs/idea.md`
  - [ ] Отметить команду `/role` как реализованную

- [ ] Обновить `docs/vision.md`
  - [ ] Обновить статус PromptLoader (планируется → реализовано)

- [ ] Создать примеры использования в `prompts/README.md`
  - [ ] Как переключить роль бота
  - [ ] Как создать свой промпт
  - [ ] Best practices для промптов

**Финальные тесты:**
```bash
# 1. Проверка с дефолтным промптом
make run
# → Отправить /role
# → Ожидается: базовая роль "AI Helpful Assistant"

# 2. Проверка со специализированным промптом
# В .env: SYSTEM_PROMPT_FILE=prompts/system_prompt_python_code_reviewer.txt
make run
# → Отправить /role
# → Ожидается: роль "Python Code Reviewer Expert"

# 3. Проверка работы специализации
# → Отправить код для ревью
# → Ожидается: ответ в стиле code reviewer
```

**Тест:** Бот показывает роль через `/role`, загружает промпты из файлов, отвечает в соответствии со специализацией

---

#### TDD Checklist

**🔴 RED Phase:**
- [ ] Все тесты написаны
- [ ] Тесты падают с понятными ошибками
- [ ] Покрыты основные сценарии и edge cases

**🟢 GREEN Phase:**
- [ ] Реализация проходит все тесты
- [ ] Минимальный код без излишеств
- [ ] Coverage не упал

**🔵 REFACTOR Phase:**
- [ ] Применены SOLID, DRY принципы
- [ ] Type hints для всех методов
- [ ] Docstrings добавлены
- [ ] `make quality` → все проверки passed

**📦 Integration:**
- [ ] Документация обновлена
- [ ] Примеры созданы
- [ ] Финальное тестирование пройдено

---

## 🚀 Быстрый старт после завершения

```bash
# 1. Клонировать и установить зависимости
make install

# 2. Настроить .env
cp .env.example .env
# Заполнить токены: TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY

# 3. Запустить бота
make run
```

---

## 📝 Примечания

- Каждая итерация должна быть завершена и протестирована перед переходом к следующей
- При возникновении проблем - обновить статус на ❌ Blocked с описанием
- После завершения итерации - обновить таблицу прогресса
- Следовать принципам из `conventions.mdc` на каждом шаге
- Коммиты после каждой успешной итерации

### TDD Workflow (для итерации 8 и далее)

**Обязательный порядок:**
1. 🔴 **RED** - Сначала тесты (должны упасть)
2. 🟢 **GREEN** - Минимальная реализация (тесты проходят)
3. 🔵 **REFACTOR** - Улучшение кода (тесты остаются зелеными)

**Не допускается:**
- ❌ Писать код без тестов
- ❌ Рефакторить на RED фазе
- ❌ Пропускать проверки `make quality`

**Рекомендуется:**
- ✅ Маленькие шаги (один тест = одна функция)
- ✅ Понятные имена тестов
- ✅ Использовать фикстуры из `conftest.py`
- ✅ Следовать `qa_conventions.mdc`

---

**Версия:** 2.0
**Создан:** 2025-01-15
**Последнее обновление:** 2025-10-11 (добавлена итерация 8 - TDD подход)
