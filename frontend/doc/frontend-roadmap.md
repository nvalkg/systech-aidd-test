# Frontend Development Roadmap

## Обзор

Данный роадмап описывает поэтапное развитие пользовательского интерфейса (frontend) для системы AIDD. Проект включает создание дашборда для визуализации статистики диалогов и веб-чата для взаимодействия с ИИ-ассистентом.

Разработка ведется итеративно небольшими спринтами, каждый из которых фокусируется на конкретной области функциональности.

## Таблица спринтов

| Код | Описание | Статус | План |
|-----|----------|--------|------|
| **FE-SPRINT-1** | Требования к дашборду и Mock API | ✅ Completed | [План](plans/s1-mock-api-plan.md) |
| **FE-SPRINT-2** | Каркас frontend проекта | ✅ Completed | [План](plans/s2-init-plan.md) |
| **FE-SPRINT-3** | Реализация dashboard | ✅ Completed | [План](plans/s3-dashboard-implement-plan.md) |
| **FE-SPRINT-4** | Реализация ИИ-чата | ✅ Completed | [План](plans/s4-chat-plan.md) |
| **FE-SPRINT-5** | Переход на реальный API | ⏸️ On Hold | - |

### Легенда статусов
- 📋 Planned — запланировано
- 🚧 In Progress — в работе
- ✅ Completed — завершено
- ⏸️ On Hold — приостановлено

---

## FE-SPRINT-1: Требования к дашборду и Mock API

**Статус:** ✅ Completed
**Дата завершения:** 17 октября 2025
**План спринта:** [s1-mock-api-plan.md](plans/s1-mock-api-plan.md)

### Цели
- Определить функциональные требования к дашборду статистики диалогов
- Спроектировать и реализовать Mock API для разработки frontend без зависимостей от backend
- Подготовить документацию и инструменты для тестирования API

### Состав работ
- Формирование емких и лаконичных функциональных требований к дашборду на основе существующих возможностей системы
- Референс для дашборда frontend\doc\frontend-reference.jpg
- Проектирование контракта API для frontend (KISS-подход: один метод для статистики под требования UI)
- Проектирование интерфейса `StatCollector` с поддержкой Mock и Real реализаций
- Реализация Mock версии сборщика статистики
- Настройка автоматической генерации документации API
- Создание entrypoint для запуска API-сервера
- Создание команд для запуска API и тестирования получения статистики

### Что реализовано

#### 📄 Документация
- **dashboard-requirements.md** - Детальные функциональные требования к дашборду с адаптацией метрик под контекст диалогов
- **api-contract-example.json** - Полный пример JSON контракта API для всех периодов
- **api-examples.md** - Примеры использования API (curl, JavaScript, React hooks)
- **frontend/README.md** - Quick start guide для frontend разработчиков

#### 💻 Backend API
- **FastAPI приложение** с автоматической OpenAPI/Swagger документацией
- **Интерфейс StatCollector** - абстракция для легкого переключения между Mock и Real реализациями
- **MockStatCollector** - генерация реалистичных тестовых данных с консистентностью
- **Эндпоинты:**
  - `GET /api/health` - health check
  - `GET /api/stats?period={day|week|month}` - получение статистики за период
- **CORS middleware** для разработки frontend

#### 📊 Метрики дашборда
4 адаптированные метрики:
1. **Total Conversations** - всего диалогов за период
2. **New Users** - новые пользователи
3. **Active Conversations** - активные диалоги
4. **Avg Messages per Conversation** - среднее сообщений на диалог

Плюс:
- График активности сообщений (24/7/30 точек для day/week/month)
- 10 последних диалогов с метаданными
- Топ 5 пользователей по активности

#### 🔧 Инфраструктура
- Добавлены зависимости: `fastapi>=0.104.0`, `uvicorn[standard]>=0.24.0`
- Команды в Makefile: `api-run`, `api-dev`, `api-test`
- Swagger UI: http://localhost:8000/docs

#### ✅ Результаты тестирования
- API успешно запускается на порту 8000
- Все эндпоинты работают корректно
- Генерация данных для разных периодов (24/7/30 точек)
- Нет ошибок линтера (ruff, mypy)

### Использование

```bash
# Запуск API
make api-dev

# Проверка
curl http://localhost:8000/api/health
curl "http://localhost:8000/api/stats?period=week"

# Swagger UI
# http://localhost:8000/docs
```

---

## FE-SPRINT-2: Каркас frontend проекта

**Статус:** ✅ Completed
**Дата завершения:** 17 октября 2025
**План спринта:** [s2-init-plan.md](plans/s2-init-plan.md)

### Цели
- Сформировать концепцию и архитектуру frontend приложения
- Выбрать оптимальный технологический стек
- Подготовить инфраструктуру для эффективной разработки

### Состав работ
- Генерация концепции frontend проекта: определение требований к пользовательскому интерфейсу (`frontend/doc/frontend-vision.md` по аналогии с `docs/vision.md`)
- Выбор технологического стека: анализ и выбор оптимального набора frontend технологий (фреймворк, библиотеки, инструменты сборки)
- Создание структуры проекта и настройка инструментов разработки (bundler, линтеры, форматтеры, type checking)
- Создание команд для запуска dev-сервера и проверки качества кода

### Что реализовано

#### 📄 Документация
- **frontend-vision.md** - Техническое видение frontend с описанием архитектуры и технологий
- **frontend/README.md** - Обновлен с Quick Start guide для Next.js разработки
- **Makefile** - Добавлены команды для frontend (fe-install, fe-dev, fe-build, fe-quality)
- **plans/s2-init-plan.md** - План спринта

#### 🏗️ Frontend приложение
- **Next.js 14+** инициализирован с TypeScript и Tailwind CSS
- **shadcn/ui** настроен с базовыми компонентами (card, button, badge, tabs)
- **TypeScript** strict mode настроен
- **ESLint + Prettier** сконфигурированы
- **API типы** созданы на основе контракта (`src/types/api.ts`)
- **API клиент** реализован (`src/lib/api.ts`)
- **Placeholder страницы** созданы (/dashboard, /chat)
- **Dark theme** применена (Inter шрифт)

#### 🛠️ Инфраструктура
- Структура проекта: `app/`, `components/`, `lib/`, `types/`
- Environment конфигурация (.env.example, .env.local)
- .gitignore для frontend
- package.json scripts: dev, build, lint, format, typecheck

#### ✅ Результаты проверок
- ✅ TypeScript typecheck passed (0 ошибок)
- ✅ ESLint passed (0 ошибок)
- ✅ Prettier formatting applied
- ✅ Production build successful
- ✅ Dev server работает на localhost:3000

### Технологический стек (выбранный)
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+ (strict mode)
- **UI Library**: shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS 4+
- **Package Manager**: pnpm

### Использование

```bash
# Установка зависимостей
make fe-install

# Запуск dev сервера
make fe-dev  # http://localhost:3000

# Проверка качества
make fe-quality  # format + lint + typecheck

# Production build
make fe-build
```

---

## FE-SPRINT-3: Реализация dashboard

**Статус:** ✅ Completed
**Дата завершения:** 17 октября 2025
**План спринта:** [s3-dashboard-implement-plan.md](plans/s3-dashboard-implement-plan.md)

### Цели
- Реализовать дашборд для визуализации статистики диалогов
- Интегрировать frontend с Mock API
- Обеспечить стабильную работу интерфейса

### Состав работ
- Реализация UI компонентов dashboard на основе референсного дизайна
- Интеграция с Mock API для получения статистики
- Реализация визуализации данных (графики, таблицы, метрики)
- Тестирование функциональности и отладка
- Адаптивная верстка для различных устройств

### Что реализовано

#### 📊 Dashboard компоненты
- **MetricCard** - карточки метрик с трендами и индикаторами направления
- **MetricCards** - grid из 4 метрик с responsive layout
- **ActivityChart** - area chart с recharts для визуализации временных рядов
- **ConversationsTable** - collapsible таблица последних 10 диалогов
- **TopUsersCard** - список топ-5 пользователей с аватарами и статистикой
- **PeriodSelector** - переключение между периодами (day/week/month)
- **DashboardHeader** - заголовок с GitHub кнопкой

#### 🔧 Технические компоненты
- **API Integration** - client-side fetching через ApiClient
- **Loading states** - skeleton placeholders для всех секций
- **Error handling** - Alert компоненты для отображения ошибок
- **Helper functions** - formatDate, formatNumber, formatRelativeTime

#### 🎨 UI компоненты (shadcn)
Добавлены: table, avatar, separator, input, collapsible, skeleton, alert

#### ✅ Результаты проверок
- ✅ TypeScript typecheck passed (0 ошибок)
- ✅ ESLint passed (0 ошибок)
- ✅ Prettier formatting applied
- ✅ API Integration работает (Mock API)
- ✅ Все компоненты отображаются корректно

### Использование

```bash
# Terminal 1: Backend API
python -m src.api_server
# Running on http://localhost:8000

# Terminal 2: Frontend dev server
cd frontend/app
pnpm dev
# Running on http://localhost:3000/dashboard
```

### Технологии использованы
- **Next.js 15** - App Router, Client Components
- **React 19** - hooks (useState, useEffect)
- **TypeScript 5** - strict mode
- **Recharts 3** - визуализация графиков
- **date-fns 4** - форматирование дат
- **shadcn/ui** - UI компоненты
- **Tailwind CSS 4** - стилизация

---

## FE-SPRINT-4: Реализация ИИ-чата

**Статус:** ✅ Completed
**Дата завершения:** 17 октября 2025
**План спринта:** [s4-chat-plan.md](plans/s4-chat-plan.md)
**Отчет о завершении:** [sprint-4-completion-report.md](sprint-4-completion-report.md)

### Цели
- Создать веб-интерфейс для взаимодействия с ИИ-ассистентом
- Реализовать API для обработки запросов чата
- Обеспечить функциональность аналитики через natural language запросы (text2sql)
- Заменить Mock API на Real API для статистики дашборда

### Состав работ
- Реализация UI чата на основе референсного дизайна
- Реализация backend API для чата (аналог Telegram-бота)
- Реализация функциональности для администратора: вопросно-ответная система по статистике диалогов
- Интеграция text-to-SQL: обработка естественноязыковых запросов → генерация SQL → выполнение → формирование ответа через LLM
- Замена MockStatCollector на RealStatCollector
- Тестирование и отладка взаимодействия

### Референсы
- **[21th-ai-chat.md](21th-ai-chat.md)** - Референс компонента чата от 21st.dev для Спринта FE-SPRINT-4

### Что реализовано

#### 📄 Backend
- **RealStatCollector** (`src/api/real_stat_collector.py`) - сборщик статистики из реальной БД
  - SQL запросы для всех метрик дашборда
  - Поддержка периодов: day, week, month
  - Тренды (сравнение с предыдущим периодом)
- **Text2SQLManager** (`src/api/text2sql_manager.py`) - менеджер text2sql запросов
  - Pipeline: question → SQL → validate → execute → format answer
  - Валидация SQL (только SELECT, безопасность)
  - Интеграция с LLM для генерации SQL и форматирования ответов
- **Text2SQL промпт** (`prompts/system_prompt_text2sql.txt`)
  - Детальная схема БД с описаниями
  - 8 примеров вопросов и SQL запросов
  - Правила безопасности
- **Chat API эндпоинты** (`src/api/main.py`)
  - `POST /api/chat/message` - отправка сообщения (normal/admin)
  - `POST /api/chat/clear` - очистка истории
  - Session-based идентификация
  - Startup инициализация с выбором Mock/Real collector

#### 💻 Frontend
- **AIChatCard** (`frontend/app/src/components/chat/AIChatCard.tsx`)
  - Адаптация референса от 21st.dev
  - Анимации (framer-motion)
  - Переключатель режимов normal/admin
  - Session ID в localStorage
  - Отображение SQL запросов (collapsible)
  - Auto-scroll, typing indicator, error handling
- **FloatingChatButton** (`frontend/app/src/components/chat/FloatingChatButton.tsx`)
  - Fixed position (bottom-right corner)
  - Открытие/закрытие с анимацией
  - Интеграция в dashboard
- **API Client** обновлен методами:
  - `sendChatMessage()` - отправка сообщения в чат
  - `clearChatHistory()` - очистка истории чата
- **API Types** добавлены:
  - `ChatMode`, `ChatMessage`, `ChatResponse`, `ChatClearRequest`

#### 🔧 Зависимости
- **Frontend:**
  - `framer-motion` - анимации
  - `shadcn/ui switch` - переключатель режимов
  - `shadcn/ui label` - подписи
- **Backend:** все зависимости уже установлены

#### ✅ Результаты тестирования
- Все импорты backend успешны
- Линтеры не выявили критичных ошибок
- Frontend TypeScript check: есть ошибки в MatrixBackground (не связаны с нашими изменениями)

### Архитектурные решения

#### Session-based Authentication
- UUID session_id в localStorage
- Backend конвертирует session_id → user_id через hash

#### Два режима работы
1. **Normal Mode**: Обычный LLM-ассистент
2. **Admin Mode**: Text2SQL для аналитики
   - SQL генерация через LLM
   - Валидация безопасности
   - Выполнение и форматирование

#### Real vs Mock Statistics
- Env variable: `USE_MOCK_STATS=true/false`
- Default: Real (если БД доступна)

### Использование

```bash
# Backend API
python -m src.api_server
# http://localhost:8000

# Frontend dev server
cd frontend/app
pnpm dev
# http://localhost:3000/dashboard

# Открыть chat через floating button в правом нижнем углу
```

### Swagger UI
http://localhost:8000/docs - документация API с возможностью тестирования эндпоинтов

---

## FE-SPRINT-5: Переход на реальный API

### Цели
- Заменить Mock реализацию на реальный сбор и обработку статистики
- Обеспечить полноценную интеграцию с production базой данных
- Завершить разработку MVP frontend

### Состав работ
- Реализация реального сборщика статистики (`RealStatCollector`)
- Интеграция с существующей базой данных проекта
- Переключение с Mock на Real реализацию с минимальными изменениями в frontend
- Финальное тестирование полного цикла работы системы
- Оптимизация производительности и запросов к БД

---

## Принципы разработки

- **Итеративность**: каждый спринт завершается работающим продуктом
- **Plan Mode**: детальное планирование выполняется перед началом каждого спринта
- **Документирование**: после завершения спринта план публикуется и линкуется в роадмапе
- **KISS принцип**: простота и лаконичность решений
- **Quality first**: акцент на качество кода и покрытие тестами

---

## История изменений

| Дата | Версия | Изменения |
|------|--------|-----------|
| 2025-10-17 | 1.4 | Завершен FE-SPRINT-4: Реализация ИИ-чата (floating button, normal/admin режимы, text2sql, Real API статистики) |
| 2025-10-17 | 1.3 | Завершен FE-SPRINT-3: Реализация dashboard (все компоненты, интеграция с API, качественный код) |
| 2025-10-17 | 1.2 | Завершен FE-SPRINT-2: Инициализация frontend проекта (Next.js + TypeScript + shadcn/ui) |
| 2025-10-17 | 1.1 | Завершен FE-SPRINT-1: Mock API для дашборда статистики |
| 2025-10-17 | 1.0 | Первоначальная версия роадмапа |
