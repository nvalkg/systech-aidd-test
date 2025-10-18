# Frontend Vision - Техническое видение frontend проекта AIDD

## Обзор

Frontend приложение для системы AIDD (AI Dialogue Dashboard) представляет собой современное веб-приложение, построенное на Next.js 14+, предоставляющее два основных интерфейса:

1. **Dashboard** - визуализация статистики диалогов Telegram-бота с LLM
2. **Web Chat** - веб-интерфейс для взаимодействия с AI-ассистентом

## Технологический стек

### Основные технологии

- **Next.js 14+** - React фреймворк с App Router
- **React 18+** - библиотека для построения пользовательских интерфейсов
- **TypeScript 5+** - типизированный JavaScript
- **shadcn/ui** - компонентная библиотека на базе Radix UI
- **Tailwind CSS** - utility-first CSS framework
- **pnpm** - быстрый пакетный менеджер

### Инструменты разработки

- **ESLint** - линтер для JavaScript/TypeScript
- **Prettier** - автоформатирование кода
- **TypeScript Compiler** - проверка типов

### Обоснование выбора

#### Next.js 14+ (App Router)
- **Производительность**: Server Components, автоматическая оптимизация
- **SEO**: Server-Side Rendering из коробки
- **Developer Experience**: Hot Module Replacement, TypeScript support
- **Routing**: File-system based routing, простой и интуитивный
- **API Routes**: Встроенная поддержка backend endpoints (для будущего)

#### TypeScript
- **Type Safety**: предотвращение ошибок на этапе разработки
- **IntelliSense**: автодополнение и подсказки в IDE
- **Рефакторинг**: безопасное переименование и изменение кода
- **Документация**: типы служат документацией к API

#### shadcn/ui
- **Не библиотека**: копирование компонентов в проект, полный контроль
- **Radix UI Primitives**: доступность (a11y), keyboard navigation
- **Customizable**: легко изменяемый дизайн через Tailwind
- **Type-safe**: полная поддержка TypeScript
- **Темная тема**: из коробки с CSS variables

#### Tailwind CSS
- **Utility-First**: быстрая разработка без написания CSS
- **Consistency**: единый дизайн-система
- **Performance**: PurgeCSS удаляет неиспользуемые стили
- **Dark Mode**: встроенная поддержка темной темы
- **Responsive**: mobile-first подход

#### pnpm
- **Скорость**: быстрее npm и yarn
- **Disk Space**: эффективное использование места через symlinks
- **Strict**: предотвращает phantom dependencies
- **Monorepo Support**: для будущего масштабирования

## Архитектура приложения

### Структура проекта

```
frontend/app/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home (redirect)
│   │   ├── dashboard/         # Дашборд статистики
│   │   │   └── page.tsx
│   │   └── chat/              # Веб-чат
│   │       └── page.tsx
│   ├── components/            # React компоненты
│   │   ├── ui/               # shadcn/ui базовые компоненты
│   │   ├── dashboard/        # Компоненты дашборда
│   │   │   ├── MetricCard.tsx
│   │   │   ├── ActivityChart.tsx
│   │   │   ├── ConversationsTable.tsx
│   │   │   └── TopUsers.tsx
│   │   └── chat/             # Компоненты чата
│   │       ├── MessageList.tsx
│   │       ├── MessageInput.tsx
│   │       └── ChatHeader.tsx
│   ├── lib/                  # Утилиты
│   │   ├── api.ts           # API клиент
│   │   └── utils.ts         # Хелперы (cn, formatDate)
│   └── types/               # TypeScript типы
│       └── api.ts           # Типы API контракта
├── public/                   # Статические файлы
├── .env.example             # Пример переменных окружения
├── .env.local               # Локальные настройки
├── next.config.js           # Конфигурация Next.js
├── tailwind.config.ts       # Конфигурация Tailwind
├── tsconfig.json            # Конфигурация TypeScript
└── package.json             # Зависимости и scripts
```

### Принципы архитектуры

#### Component-Driven Development
- **Модульность**: каждый компонент решает одну задачу
- **Переиспользуемость**: компоненты UI используются в разных местах
- **Изоляция**: компоненты не знают друг о друге напрямую
- **Composability**: сложные UI собираются из простых компонентов

#### Разделение ответственности (Separation of Concerns)
- **app/**: маршрутизация и layout
- **components/**: переиспользуемые UI компоненты
- **lib/**: бизнес-логика, API клиенты, утилиты
- **types/**: TypeScript интерфейсы и типы

#### Server Components First
- По умолчанию все компоненты - Server Components
- Client Components (`'use client'`) только где необходимо:
  - Интерактивность (onClick, useState)
  - Browser APIs (localStorage, window)
  - React hooks (useEffect, useContext)

## Интеграция с Backend

### API клиент

**Файл**: `src/lib/api.ts`

```typescript
export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL) {
    this.baseUrl = baseUrl;
  }

  async getStats(period: Period): Promise<DashboardStats> {
    // Запрос к Backend API
  }

  async healthCheck(): Promise<{ status: string }> {
    // Health check
  }
}
```

### Этапы интеграции

**Этап 1: Mock API (FE-SPRINT-2, FE-SPRINT-3)**
- Frontend работает с существующим Mock API (FastAPI)
- URL: `http://localhost:8000`
- Эндпоинты: `/api/health`, `/api/stats?period={day|week|month}`

**Этап 2: Real API (FE-SPRINT-5)**
- Замена MockStatCollector на RealStatCollector в Backend
- Frontend код не меняется (благодаря StatCollector интерфейсу)
- Подключение к production базе данных

### CORS конфигурация

Backend (FastAPI) настроен для CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production: конкретные домены
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Типизация данных

### API контракт

**Файл**: `src/types/api.ts`

```typescript
export type Period = "day" | "week" | "month";

export interface MetricCard {
  title: string;
  value: string;
  trend: number;
  trend_label: string;
  description: string;
}

export interface TimeSeriesPoint {
  timestamp: string;  // ISO 8601
  value: number;
}

export interface ConversationItem {
  conversation_id: number;
  user_id: number;
  messages_count: number;
  last_activity: string;  // ISO 8601
  created_at: string;  // ISO 8601
}

export interface TopUser {
  user_id: number;
  messages_count: number;
  conversations_count: number;
}

export interface DashboardStats {
  metrics: MetricCard[];
  activity_chart: TimeSeriesPoint[];
  recent_conversations: ConversationItem[];
  top_users: TopUser[];
  period: Period;
}
```

### Принципы типизации

- **Strict Mode**: `tsconfig.json` с strict: true
- **No Any**: избегаем `any`, используем `unknown` где необходимо
- **Interface > Type**: предпочтение интерфейсам для объектов
- **Exported Types**: все типы API экспортируются для переиспользования

## UI/UX Принципы

### Дизайн система

#### Темная тема (по умолчанию)
- Основана на референсе: `frontend/doc/frontend-reference.jpg`
- CSS Variables для гибкой кастомизации
- Цветовая схема: Slate (shadcn/ui)

#### Типография
- **Font**: Inter (Google Fonts)
- **Размеры**:
  - H1: 4xl (36px)
  - H2: 3xl (30px)
  - Body: base (16px)
  - Small: sm (14px)

#### Spacing
- Tailwind spacing scale: 4px базовая единица
- Consistent spacing между элементами

#### Компоненты
- **Card**: контейнер для метрик, таблиц
- **Badge**: статусы, категории
- **Button**: primary, secondary, ghost варианты
- **Tabs**: переключение периодов (day/week/month)

### Адаптивность

- **Desktop First**: приоритет на desktop (референс)
- **Minimum Width**: 1024px
- **Tablet**: graceful degradation
- **Mobile**: not a priority for MVP

### Производительность

- **Code Splitting**: автоматически через Next.js
- **Image Optimization**: next/image для картинок
- **Lazy Loading**: динамический импорт для тяжелых компонентов
- **Bundle Size**: мониторинг размера бандла

## Качество кода

### Инструменты

#### ESLint
- **Base Config**: `next/core-web-vitals`
- **Extended**: `prettier` для совместимости
- **Custom Rules**:
  - `no-console`: warn (разрешены warn, error)
  - `@typescript-eslint/no-unused-vars`: error

#### Prettier
- **semi**: true
- **singleQuote**: false
- **tabWidth**: 2
- **printWidth**: 80
- **trailingComma**: "es5"

#### TypeScript
- **strict**: true
- **noUncheckedIndexedAccess**: true
- **noUnusedLocals**: true
- **noUnusedParameters**: true
- **noImplicitReturns**: true

### Команды качества

```bash
# Локально
pnpm format         # Prettier форматирование
pnpm lint           # ESLint проверка
pnpm typecheck      # TypeScript проверка

# Через Makefile (из корня проекта)
make fe-format      # Prettier форматирование
make fe-lint        # ESLint проверка
make fe-typecheck   # TypeScript проверка
make fe-quality     # Все проверки сразу
```

### Метрики качества

| Метрика | Цель | Статус |
|---------|------|--------|
| ESLint errors | 0 | 🎯 Target |
| TypeScript errors | 0 | 🎯 Target |
| Type coverage | 100% | 🎯 Target |
| Unused code | 0 | 🎯 Target |

## Принципы разработки

### KISS (Keep It Simple, Stupid)
- Простые компоненты без overengineering
- Прямолинейная логика
- Минимум абстракций

### DRY (Don't Repeat Yourself)
- Переиспользуемые UI компоненты
- Общие утилиты в `lib/`
- Типы API в одном месте

### Type Safety First
- Все функции и компоненты типизированы
- Props интерфейсы для React компонентов
- Строгий TypeScript без `any`

### Component Composition
- Маленькие, фокусированные компоненты
- Композиция вместо наследования
- Props для кастомизации

## Workflow разработки

### Локальная разработка

```bash
# 1. Установка зависимостей
make fe-install    # или: cd frontend/app && pnpm install

# 2. Запуск Backend API (в отдельном терминале)
make api-dev       # http://localhost:8000

# 3. Запуск Frontend dev server
make fe-dev        # http://localhost:3000

# 4. Разработка с hot reload
# Изменения в коде автоматически обновляются в браузере
```

### Проверка качества

```bash
# Перед коммитом (обязательно!)
make fe-quality    # format + lint + typecheck

# Или по отдельности
make fe-format     # Автоформатирование
make fe-lint       # Проверка линтером
make fe-typecheck  # Проверка типов
```

### Build для production

```bash
make fe-build      # Next.js build
# Результат: .next/ директория с оптимизированным кодом
```

## Будущие улучшения

### FE-SPRINT-3: Dashboard реализация
- Компоненты метрик (MetricCard)
- График активности (ActivityChart с recharts/chart.js)
- Таблица диалогов (ConversationsTable)
- Топ пользователей (TopUsers)

### FE-SPRINT-4: Web Chat
- MessageList с виртуализацией
- MessageInput с markdown support
- Real-time updates (polling или WebSockets)
- Chat history

### FE-SPRINT-5: Production готовность
- Real API интеграция
- Error boundaries
- Loading states
- Analytics (Google Analytics / Plausible)

### Возможные направления (после MVP)
- **Testing**: Vitest + React Testing Library
- **Storybook**: изолированная разработка компонентов
- **E2E тесты**: Playwright для критичных flows
- **Internationalization**: i18n для мультиязычности
- **PWA**: Progressive Web App возможности
- **Performance monitoring**: Web Vitals tracking

## Документация

### Для разработчиков

- **frontend/README.md** - Quick start, команды, структура
- **frontend/doc/frontend-vision.md** - этот документ
- **frontend/doc/dashboard-requirements.md** - требования к дашборду
- **frontend/doc/api-examples.md** - примеры работы с API
- **frontend/doc/frontend-roadmap.md** - план разработки по спринтам

### Конвенции кодирования

- **Именование файлов**: PascalCase для компонентов (`MetricCard.tsx`)
- **Именование переменных**: camelCase (`userName`)
- **Именование типов**: PascalCase (`DashboardStats`)
- **Именование констант**: UPPER_SNAKE_CASE (`API_BASE_URL`)

### Структура компонентов

```tsx
// 1. Imports
import { useState } from "react";
import { Card } from "@/components/ui/card";
import type { MetricCard } from "@/types/api";

// 2. Types
interface MetricCardProps {
  metric: MetricCard;
}

// 3. Component
export function MetricCardComponent({ metric }: MetricCardProps) {
  // 3.1. Hooks
  const [isExpanded, setIsExpanded] = useState(false);

  // 3.2. Handlers
  const handleClick = () => {
    setIsExpanded(!isExpanded);
  };

  // 3.3. Render
  return (
    <Card onClick={handleClick}>
      {/* JSX */}
    </Card>
  );
}
```

## Заключение

Frontend проект AIDD строится на современном, проверенном стеке технологий с фокусом на:

- ✅ **Type Safety** - TypeScript strict mode
- ✅ **Developer Experience** - Hot reload, TypeScript IntelliSense
- ✅ **Performance** - Next.js оптимизации
- ✅ **UI Quality** - shadcn/ui компоненты, темная тема
- ✅ **Code Quality** - ESLint, Prettier, TypeScript
- ✅ **Maintainability** - чистая архитектура, хорошая документация

Проект готов к итеративному развитию через спринты с постепенным добавлением функциональности.

---

**Документ создан:** 2025-10-17
**Версия:** 1.0
**Статус:** FE-SPRINT-2 Initialization
