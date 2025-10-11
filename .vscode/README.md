# VSCode/Cursor IDE Configuration

Этот каталог содержит конфигурационные файлы для удобной работы с проектом в VSCode/Cursor IDE.

## 📦 Необходимые расширения

Установите следующие расширения для полноценной работы:

1. **Python** (`ms-python.python`) - основная поддержка Python
2. **Ruff** (`charliermarsh.ruff`) - линтер и форматтер
3. **Pylance** (`ms-python.vscode-pylance`) - language server для Python
4. **Python Debugger** (`ms-python.debugpy`) - отладчик Python

### Быстрая установка расширений

Нажмите `Ctrl+Shift+P` и выберите `Extensions: Install Extensions`, затем установите:
```
ms-python.python
charliermarsh.ruff
ms-python.vscode-pylance
ms-python.debugpy
```

---

## 🚀 Как использовать

### 1️⃣ Запуск и отладка бота (Run & Debug)

Перейдите на панель **Run and Debug** (`Ctrl+Shift+D`) и выберите конфигурацию:

#### **▶️ Run Bot**
- Запускает бота в обычном режиме
- `justMyCode: true` - останавливается только на ваших breakpoints

#### **🐛 Debug Bot**
- Запускает бота с полной отладкой
- `justMyCode: false` - позволяет заходить в код библиотек

#### **🧪 Debug Current Test File**
- Отлаживает текущий открытый тест-файл
- Удобно для разработки конкретного теста

#### **🧪 Debug All Tests**
- Запускает все тесты с coverage
- Позволяет отлаживать весь тестовый набор

#### **🧪 Debug Test with Pytest Breakpoint**
- Специальный режим для работы с `pytest.set_trace()`
- `--capture=no` отключает перехват вывода

**Как запустить:**
1. Откройте файл (для текущего теста)
2. Установите breakpoint (F9)
3. Нажмите F5 или выберите конфигурацию из списка
4. Используйте F10 (Step Over), F11 (Step Into), Shift+F11 (Step Out)

---

### 2️⃣ Задачи (Tasks)

Запускайте задачи через `Terminal > Run Task...` (`Ctrl+Shift+P` → "Tasks: Run Task") или используйте горячие клавиши.

#### Тестирование

- **🧪 Run All Tests** (Default Test Task)
  ```bash
  make test
  ```
  - Быстрая клавиша: `Ctrl+Shift+B` → выбрать тест

- **🧪 Run Tests with Coverage**
  ```bash
  uv run pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
  ```
  - Создаёт HTML отчёт в `htmlcov/index.html`

- **🧪 Run Current Test File**
  ```bash
  uv run pytest ${file} -v -s
  ```
  - Запускает только текущий открытый файл

#### Качество кода

- **✨ Format Code**
  ```bash
  make format
  ```
  - Автоформатирование через Ruff

- **🔍 Lint Code**
  ```bash
  make lint
  ```
  - Проверка на ошибки через Ruff
  - Результаты попадают в Problems panel (`Ctrl+Shift+M`)

- **🔍 Type Check**
  ```bash
  make typecheck
  ```
  - Проверка типов через MyPy
  - Результаты в Problems panel

- **✅ Quality Check (All)** (Default Build Task)
  ```bash
  make quality
  ```
  - Запускает: format + lint + typecheck + test
  - Быстрая клавиша: `Ctrl+Shift+B`

#### Управление проектом

- **▶️ Run Bot**
  ```bash
  make dev
  ```
  - Запускает бота через терминал

- **📦 Install Dependencies**
  ```bash
  make install
  ```
  - Установка зависимостей через uv

- **🧹 Clean Cache**
  ```bash
  make clean
  ```
  - Удаление кеша Python

---

### 3️⃣ Настройки проекта (Settings)

Файл `settings.json` автоматически настраивает:

#### Python окружение
- **Интерпретатор**: `.venv/Scripts/python.exe`
- **PYTHONPATH**: автоматически устанавливается

#### Тестирование
- **Pytest** включён по умолчанию
- Автоматическое обнаружение тестов при сохранении
- Coverage при запуске

#### Форматирование и линтинг
- **Ruff** как форматтер по умолчанию
- Форматирование при сохранении (`Ctrl+S`)
- Автоматическая сортировка импортов
- Автоисправление ошибок

#### MyPy
- Type checking включён
- Использует настройки из `pyproject.toml`

#### Редактор
- Line length: 100 символов (ruler)
- Tab size: 4 пробела
- Удаление trailing whitespace

---

## 🎯 Быстрый старт

### Первый запуск

1. **Установите зависимости:**
   ```bash
   # Через задачу
   Ctrl+Shift+P → Tasks: Run Task → 📦 Install Dependencies

   # Или через терминал
   make install
   ```

2. **Создайте `.env` файл** с необходимыми переменными:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   OPENROUTER_API_KEY=your_key_here
   DEFAULT_MODEL=openai/gpt-4-turbo
   ```

3. **Запустите бота:**
   ```bash
   # Через Run & Debug (F5)
   Ctrl+Shift+D → ▶️ Run Bot → F5

   # Или через задачу
   Ctrl+Shift+P → Tasks: Run Task → ▶️ Run Bot
   ```

4. **Запустите тесты:**
   ```bash
   # Через Test Explorer
   Открыть Test Explorer → Run All Tests

   # Или через задачу
   Ctrl+Shift+B → 🧪 Run All Tests
   ```

---

## 📝 Полезные горячие клавиши

### Отладка
- `F5` - Start/Continue debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out
- `Shift+F5` - Stop debugging

### Задачи
- `Ctrl+Shift+B` - Run default build task (Quality Check)
- `Ctrl+Shift+P` → "Tasks: Run Task" - Выбор задачи

### Тестирование
- `Ctrl+Shift+P` → "Test: Run All Tests" - через Test Explorer
- `Ctrl+Shift+P` → "Test: Debug Test at Cursor" - отладка теста под курсором

### Навигация
- `Ctrl+Shift+M` - Show Problems panel
- `Ctrl+` ` - Toggle terminal
- `Ctrl+Shift+E` - Explorer
- `Ctrl+Shift+D` - Run and Debug

---

## 🔧 Troubleshooting

### Проблема: Python интерпретатор не найден

**Решение:**
1. Установите виртуальное окружение:
   ```bash
   make install
   ```
2. Перезагрузите окно: `Ctrl+Shift+P` → "Developer: Reload Window"
3. Выберите интерпретатор: `Ctrl+Shift+P` → "Python: Select Interpreter" → `.venv`

### Проблема: Тесты не обнаруживаются

**Решение:**
1. Откройте Output panel: `Ctrl+Shift+U`
2. Выберите "Python Test Log" в dropdown
3. Проверьте ошибки
4. Попробуйте: `Ctrl+Shift+P` → "Test: Refresh Tests"

### Проблема: Ruff не форматирует код

**Решение:**
1. Убедитесь, что расширение Ruff установлено
2. Проверьте настройки: `.vscode/settings.json`
3. Попробуйте вручную: `Ctrl+Shift+P` → "Format Document" (`Alt+Shift+F`)

### Проблема: Breakpoints не срабатывают

**Решение:**
1. Проверьте, что используете конфигурацию с `justMyCode: false`
2. Убедитесь, что код достижим (не пропускается условием)
3. Попробуйте `import pdb; pdb.set_trace()` как fallback

---

## 📚 Дополнительная информация

- [Официальная документация Python в VSCode](https://code.visualstudio.com/docs/python/python-tutorial)
- [Документация Pytest](https://docs.pytest.org/)
- [Документация Ruff](https://docs.astral.sh/ruff/)
- [Документация MyPy](https://mypy.readthedocs.io/)

---

**Версия:** 1.0
**Дата:** 2025-10-11
**Совместимость:** VSCode 1.80+, Cursor IDE
