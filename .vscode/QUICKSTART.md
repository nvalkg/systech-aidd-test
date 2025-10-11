# 🚀 Быстрый старт в VSCode/Cursor

> **5 минут до запуска проекта!**

## ✅ Шаг 1: Установка расширений (автоматически)

При открытии проекта IDE предложит установить расширения - **нажмите "Install"**:
- ✅ Python
- ✅ Ruff
- ✅ Pylance
- ✅ Python Debugger

*Или вручную: Ctrl+Shift+P → "Extensions: Show Recommended Extensions"*

---

## ✅ Шаг 2: Выбор интерпретатора

1. Нажмите **Ctrl+Shift+P**
2. Введите: **"Python: Select Interpreter"**
3. Выберите: **`.venv\Scripts\python.exe`**

*Если .venv нет, сначала запустите: `make install` в терминале*

---

## ✅ Шаг 3: Создание .env файла

1. Скопируйте `.env.example` в `.env`:
   ```bash
   cp .env.example .env
   ```

2. Отредактируйте `.env` и добавьте токены:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_from_botfather
   OPENROUTER_API_KEY=your_key_from_openrouter
   ```

---

## ✅ Шаг 4: Запуск бота

### Способ 1: Run & Debug (рекомендуется)

1. Откройте панель **Run and Debug** (**Ctrl+Shift+D**)
2. Выберите **"▶️ Run Bot"**
3. Нажмите **F5**

### Способ 2: Через задачи

1. Нажмите **Ctrl+Shift+P**
2. Выберите **"Tasks: Run Task"**
3. Выберите **"▶️ Run Bot"**

---

## ✅ Шаг 5: Запуск тестов

### Test Explorer (визуально)

1. Откройте панель **Testing** (значок колбы слева)
2. Нажмите **"Run All Tests"** (▶️)
3. Просмотрите результаты

### Debug тестов

1. Откройте файл с тестом (например, `tests/test_config.py`)
2. Поставьте **breakpoint** (F9)
3. **Run & Debug** → **"🧪 Debug Current Test File"**
4. Нажмите **F5**

---

## 🎯 Основные горячие клавиши

| Действие | Клавиша |
|----------|---------|
| **Запуск/Отладка** | `F5` |
| **Breakpoint** | `F9` |
| **Step Over** | `F10` |
| **Step Into** | `F11` |
| **Задачи** | `Ctrl+Shift+B` |
| **Форматировать** | `Alt+Shift+F` |
| **Проблемы (Problems)** | `Ctrl+Shift+M` |
| **Терминал** | `` Ctrl+` `` |
| **Test Explorer** | Левая панель → колба |

---

## 🛠️ Полезные задачи (Ctrl+Shift+B)

- **✅ Quality Check (All)** - все проверки перед PR
- **🧪 Run All Tests** - запуск тестов с coverage
- **✨ Format Code** - форматирование через Ruff
- **🔍 Lint Code** - проверка линтером
- **🔍 Type Check** - проверка типов MyPy

---

## 📝 Автоматические фичи

При работе в IDE автоматически:

✅ **Форматирование при сохранении** (Ctrl+S)
✅ **Автоисправление ошибок** (Ruff)
✅ **Сортировка импортов** (isort)
✅ **Подсветка ошибок типов** (MyPy)
✅ **Автодополнение** (Pylance)
✅ **Test discovery** (Pytest)

---

## ❓ Проблемы?

### Интерпретатор не найден
```bash
make install
# Потом: Ctrl+Shift+P → "Developer: Reload Window"
```

### Тесты не обнаруживаются
```bash
Ctrl+Shift+P → "Test: Refresh Tests"
```

### Breakpoints не работают
- Используйте конфигурацию **"🐛 Debug Bot"** (justMyCode: false)

---

## 📚 Больше информации

- **Полная документация:** [README.md](README.md)
- **Настройки IDE:** [.vscode/settings.json](settings.json)
- **Конфигурации запуска:** [.vscode/launch.json](launch.json)
- **Задачи:** [.vscode/tasks.json](tasks.json)

---

**Готово! Приятной разработки! 🚀**
