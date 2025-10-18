# Frontend Development

Этот каталог содержит документацию и ресурсы для разработки frontend части проекта AIDD.

## Структура

```
frontend/
├── app/                          # Next.js приложение
│   ├── src/
│   │   ├── app/                 # App Router (pages)
│   │   ├── components/          # React компоненты
│   │   ├── lib/                 # Утилиты и API клиент
│   │   └── types/               # TypeScript типы
│   ├── public/                  # Статические файлы
│   └── package.json
├── doc/                          # Документация
│   ├── dashboard-requirements.md # Функциональные требования к дашборду
│   ├── api-contract-example.json # Пример API контракта
│   ├── api-examples.md          # Примеры использования API
│   ├── frontend-vision.md       # Техническое видение frontend
│   ├── frontend-roadmap.md      # Роадмап развития frontend
│   ├── frontend-reference.jpg   # Референс дизайна дашборда
│   ├── sprint-1-completion-report.md # Отчет о завершении спринта 1
│   └── plans/                   # Планы спринтов
│       ├── s1-mock-api-plan.md  # План FE-SPRINT-1
│       └── s2-init-plan.md      # План FE-SPRINT-2
└── README.md                     # Этот файл
```

## Quick Start: Mock API

### Установка зависимостей

```bash
uv sync
```

### Запуск API сервера

```bash
# Через make (рекомендуется)
make api-dev

# Или напрямую
uv run uvicorn src.api.main:app --reload --port 8000
```

### Проверка работоспособности

```bash
# Health check
curl http://localhost:8000/api/health

# Получить статистику за неделю
curl "http://localhost:8000/api/stats?period=week" | python -m json.tool
```

### Swagger UI

После запуска сервера откройте в браузере:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Доступные эндпоинты

### GET /api/health
Health check - проверка доступности API

**Ответ:**
```json
{
  "status": "ok"
}
```

### GET /api/stats
Получить статистику дашборда

**Параметры:**
- `period` (string): Период для статистики - `"day"`, `"week"`, или `"month"` (по умолчанию: `"week"`)

**Примеры:**
```bash
# За день (24 почасовых точки)
curl "http://localhost:8000/api/stats?period=day"

# За неделю (7 посуточных точек)
curl "http://localhost:8000/api/stats?period=week"

# За месяц (30 посуточных точек)
curl "http://localhost:8000/api/stats?period=month"
```

## Документация

- **[Функциональные требования](doc/dashboard-requirements.md)** - Детальное описание требований к дашборду
- **[Примеры API](doc/api-examples.md)** - Примеры запросов на curl и JavaScript
- **[Frontend Roadmap](doc/frontend-roadmap.md)** - Роадмап развития frontend
- **[Отчет Sprint 1](doc/sprint-1-completion-report.md)** - Результаты первого спринта

## Спринты

### ✅ FE-SPRINT-1: Mock API (Completed)
- Функциональные требования к дашборду
- Mock API с тестовыми данными
- Swagger документация
- [Детали](doc/plans/s1-mock-api-plan.md)

### 🚧 FE-SPRINT-2: Каркас frontend проекта (In Progress)
- Next.js 14+ инициализация
- TypeScript strict mode
- shadcn/ui компоненты
- Настройка инструментов разработки
- [План](doc/plans/s2-init-plan.md)

### 📋 FE-SPRINT-3: Реализация dashboard (Planned)
- UI компоненты дашборда
- Интеграция с Mock API
- Визуализация данных

## Для Frontend разработчиков

### Контракт API

Полный пример структуры данных: [api-contract-example.json](doc/api-contract-example.json)

### Основные сущности

**MetricCard** - Карточка метрики:
```typescript
interface MetricCard {
  title: string;
  value: string;
  trend: number;
  trend_label: string;
  description: string;
}
```

**TimeSeriesPoint** - Точка графика:
```typescript
interface TimeSeriesPoint {
  timestamp: string; // ISO 8601
  value: number;
}
```

**ConversationItem** - Элемент списка диалогов:
```typescript
interface ConversationItem {
  conversation_id: number;
  user_id: number;
  messages_count: number;
  last_activity: string; // ISO 8601
  created_at: string; // ISO 8601
}
```

**TopUser** - Пользователь в топе:
```typescript
interface TopUser {
  user_id: number;
  messages_count: number;
  conversations_count: number;
}
```

### Метрики дашборда

1. **Total Conversations** - Всего диалогов за период
2. **New Users** - Новые пользователи за период
3. **Active Conversations** - Активные диалоги за период
4. **Avg Messages per Conversation** - Среднее сообщений на диалог

## Quick Start: Frontend (Next.js)

### Установка зависимостей

```bash
# Из корня проекта
make fe-install

# Или напрямую
cd frontend/app && pnpm install
```

### Запуск dev сервера

```bash
# Из корня проекта (рекомендуется)
make fe-dev

# Или напрямую
cd frontend/app && pnpm dev
```

Frontend будет доступен по адресу: **http://localhost:3000**

### Проверка качества кода

```bash
# Из корня проекта
make fe-format     # Prettier форматирование
make fe-lint       # ESLint проверка
make fe-typecheck  # TypeScript проверка
make fe-quality    # Все проверки сразу

# Или из директории app/
cd frontend/app
pnpm format
pnpm lint
pnpm typecheck
```

### Build для production

```bash
make fe-build

# Или
cd frontend/app && pnpm build
```

## Полезные команды

### Backend API
```bash
make api-dev      # Запуск с auto-reload
make api-run      # Обычный запуск
make api-test     # Тест эндпоинта
```

### Frontend (из корня проекта)
```bash
make fe-install   # Установка зависимостей
make fe-dev       # Dev сервер (localhost:3000)
make fe-build     # Production build
make fe-lint      # ESLint проверка
make fe-format    # Prettier форматирование
make fe-typecheck # TypeScript проверка
make fe-quality   # Все проверки качества
```

### Backend (качество кода)
```bash
make format       # Форматирование
make lint         # Линтер
make typecheck    # Проверка типов
```

## Технологический стек

### Backend API
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Python 3.11+** - Runtime
- **Dataclasses** - Data models

### Frontend
- **Next.js 14+** - React фреймворк с App Router
- **React 19** - UI библиотека
- **TypeScript 5+** - Типизированный JavaScript
- **shadcn/ui** - Компонентная библиотека
- **Tailwind CSS** - Utility-first CSS
- **pnpm** - Пакетный менеджер

Подробнее: [frontend/doc/frontend-vision.md](doc/frontend-vision.md)

## Конвенции разработки (Frontend)

- **TypeScript strict mode** - строгая типизация
- **ESLint** - проверка кода
- **Prettier** - автоформатирование
- **Component-driven** - компонентный подход
- **Dark theme** - темная тема по умолчанию

## Следующие шаги

1. ✅ **FE-SPRINT-1**: Mock API для дашборда - завершен
2. 🚧 **FE-SPRINT-2**: Инициализация frontend проекта - в процессе
3. 📋 **FE-SPRINT-3**: Реализация дашборда с интеграцией Mock API
4. 📋 **FE-SPRINT-4**: Реализация веб-чата с AI
5. 📋 **FE-SPRINT-5**: Переход на реальный API

## Поддержка

Для вопросов и предложений смотрите документацию в `doc/` или создайте issue в репозитории.
