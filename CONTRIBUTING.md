# Руководство по участию в разработке

Спасибо за интерес к проекту! Этот документ описывает процесс разработки.

## 🚀 Начало работы

### 1. Форк и клонирование

```bash
# Форк репозитория на GitHub, затем:
git clone https://github.com/YOUR_USERNAME/systech-aidd-test.git
cd systech-aidd-test
```

### 2. Установка зависимостей

```bash
# Установка uv (если еще не установлен)
# Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установка зависимостей проекта
make install
```

### 3. Настройка окружения

```bash
# Создание .env файла
cp .env.example .env
# Добавьте свои токены в .env:
# - TELEGRAM_BOT_TOKEN (получить у @BotFather)
# - OPENROUTER_API_KEY (получить на openrouter.ai)
```

## 📝 Workflow разработки

### 1. Создание ветки

```bash
git checkout -b feature/my-new-feature
# или
git checkout -b fix/my-bug-fix
```

### 2. Разработка

1. **Напишите код** согласно [conventions.mdc](.cursor/rules/conventions.mdc)
2. **Добавьте тесты** для нового функционала
3. **Запустите проверки качества:**

```bash
make quality  # format + lint + typecheck + test
```

### 3. Коммиты

Используем conventional commits:

```bash
git commit -m "feat: добавлена новая команда /stats"
git commit -m "fix: исправлена обработка пустых сообщений"
git commit -m "refactor: улучшен метод _get_user_info"
git commit -m "test: добавлены тесты для telegram_bot"
git commit -m "docs: обновлена документация README"
```

**Типы коммитов:**
- `feat:` - новый функционал
- `fix:` - исправление бага
- `refactor:` - рефакторинг без изменения функционала
- `test:` - добавление или изменение тестов
- `docs:` - изменения в документации
- `style:` - форматирование, точки с запятой и т.д.
- `perf:` - улучшение производительности
- `chore:` - обновление зависимостей, конфигурации и т.д.

### 4. Pull Request

1. Убедитесь, что `make quality` проходит без ошибок
2. Push в свой форк: `git push origin feature/my-new-feature`
3. Создайте Pull Request на GitHub
4. Опишите изменения и их причину
5. Дождитесь прохождения CI/CD проверок

## ✅ Требования к PR

Перед созданием PR проверьте:

- [ ] `make format` - код отформатирован
- [ ] `make lint` - 0 ошибок линтера
- [ ] `make typecheck` - все type hints на месте
- [ ] `make test` - все тесты проходят
- [ ] Coverage не упал (цель >80%, текущий 95%)
- [ ] Добавлены тесты для нового функционала
- [ ] Документация обновлена (если нужно)
- [ ] CI/CD проверки проходят (автоматически)

## 🏗️ Архитектура

### Принципы

- **KISS** - максимальная простота, никакого оверинжиниринга
- **1 класс = 1 файл** - строгое ООП
- **SOLID** - Single Responsibility Principle
- **DRY** - Don't Repeat Yourself
- **Type hints** - для всех публичных методов
- **Async/await** - для всех операций ввода-вывода

### Структура компонентов

```
TelegramBot → ConversationManager → LLMClient
              ↓
          HistoryStorage + MessageFormatter
              ↓
            Models (dataclasses)
```

Подробнее: [docs/vision.md](docs/vision.md)

### Ответственность модулей

- **Config** - загрузка и валидация конфигурации из .env
- **Models** - структуры данных (dataclasses)
- **HistoryStorage** - хранение истории сообщений
- **MessageFormatter** - форматирование для LLM API
- **ConversationManager** - оркестрация диалога
- **LLMClient** - взаимодействие с OpenRouter API
- **TelegramBot** - обработка команд и сообщений Telegram
- **main.py** - точка входа, инициализация компонентов

## 🧪 Тестирование

### Написание тестов

```python
# tests/test_my_module.py
import pytest
from src.my_module import MyClass

def test_my_function():
    """Тест: описание сценария"""
    # Arrange - подготовка
    obj = MyClass()

    # Act - действие
    result = obj.my_function()

    # Assert - проверка
    assert result == expected_value
```

### Async тесты

```python
@pytest.mark.asyncio
async def test_async_function():
    """Тест async функции"""
    result = await my_async_function()
    assert result == expected
```

### Мокирование

```python
from unittest.mock import Mock, AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    """Тест с мокированием зависимостей"""
    mock_dependency = Mock()
    mock_dependency.method.return_value = "test"

    # Для async методов используйте AsyncMock
    mock_async = AsyncMock()
    mock_async.async_method.return_value = "test"
```

### Фикстуры

Используйте общие фикстуры из `tests/conftest.py`:

```python
def test_with_fixture(valid_env, monkeypatch):
    """Тест с использованием фикстуры"""
    # valid_env уже настроил окружение
    # monkeypatch для изменения переменных окружения
    monkeypatch.setenv("MY_VAR", "test_value")
```

### Запуск тестов

```bash
# Все тесты с coverage
make test

# Только конкретный модуль
uv run pytest tests/test_config.py -v

# Только конкретный тест
uv run pytest tests/test_config.py::test_config_invalid_max_tokens -v

# С HTML отчетом coverage
uv run pytest tests/ --cov=src --cov-report=html
# Откройте htmlcov/index.html в браузере
```

## 📊 Coverage

- Цель: **>80%** общий coverage
- Текущий: **95%**
- Критичные модули: **100%** (config, models)
- Бизнес-логика: **>90%** (llm_client, conversation_manager)

Проверка coverage:
```bash
make test
```

HTML отчет:
```bash
uv run pytest --cov=src --cov-report=html
# Откройте htmlcov/index.html
```

## 🔧 Команды Makefile

```bash
make install    # Установка зависимостей через uv
make format     # Автоформатирование кода (ruff format)
make lint       # Проверка линтером (ruff check)
make typecheck  # Проверка типов (mypy)
make test       # Запуск тестов с coverage
make quality    # Все проверки разом (обязательно перед PR!)
make run        # Запуск бота
make dev        # Запуск с использованием uv run
make clean      # Очистка кэшей и временных файлов
```

## 🐛 Отладка

### Логирование

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Отладочная информация")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка", exc_info=True)
```

### Запуск с отладкой

Установите `LOG_LEVEL=DEBUG` в `.env`:

```bash
# В .env
LOG_LEVEL=DEBUG

# Запуск
make run
```

## 🔍 Code Review

### Что проверяют в PR

1. **Архитектура:**
   - Соблюдение SOLID (особенно SRP)
   - Отсутствие дублирования (DRY)
   - Слабая связанность между компонентами

2. **Код:**
   - Type hints для всех публичных методов
   - Docstrings для классов и сложных методов
   - Понятные имена переменных и функций
   - Обработка ошибок

3. **Тесты:**
   - Покрытие нового функционала
   - Arrange-Act-Assert структура
   - Использование моков для внешних зависимостей

4. **Документация:**
   - Обновление README при изменении API
   - Комментарии для сложной логики

## 🚫 Что НЕ нужно делать

- ❌ Не коммитьте `.env` файл (токены и секреты)
- ❌ Не коммитьте `__pycache__`, `.pytest_cache`, `.mypy_cache`
- ❌ Не создавайте PR без прохождения `make quality`
- ❌ Не игнорируйте ошибки линтера или mypy
- ❌ Не удаляйте существующие тесты без причины
- ❌ Не добавляйте зависимости без обсуждения
- ❌ Не пишите код без type hints
- ❌ Не создавайте "god objects" (нарушение SRP)

## 📚 Документы для изучения

Перед началом разработки изучите:

1. [roadmap.md](docs/roadmap.md) - дорожная карта проекта
2. [vision.md](docs/vision.md) - техническое видение проекта
3. [conventions.mdc](.cursor/rules/conventions.mdc) - правила кодирования
4. [workflow.mdc](.cursor/rules/workflow.mdc) - процесс разработки
5. [tasklists/](docs/tasklists/) - детальные планы спринтов

## 🆘 Нужна помощь?

- **Вопросы по коду:** создайте Issue на GitHub
- **Обсуждение PR:** пишите в комментариях к Pull Request
- **Предложения:** создайте Issue с меткой "enhancement"
- **Баги:** создайте Issue с меткой "bug"

## 🎯 Приоритеты разработки

Текущие приоритеты:

1. ✅ Качество кода (SOLID, DRY, type hints)
2. ✅ Покрытие тестами (>80%)
3. ✅ Документация
4. 🔄 CI/CD автоматизация
5. ⏳ Новый функционал (после завершения рефакторинга)

## 🎉 Спасибо!

Спасибо за вклад в проект! Каждый PR делает проект лучше. 🚀

---

**Версия:** 1.0
**Создан:** 2025-10-11
**Базируется на:** [workflow_tech_debt.mdc](.cursor/rules/workflow_tech_debt.mdc)
