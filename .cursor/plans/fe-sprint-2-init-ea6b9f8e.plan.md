<!-- ea6b9f8e-f6de-4232-aaaf-d4b79cd7fdca 5d46e85d-00b9-4daf-887e-d52581487eff -->
# FE-SPRINT-2: Инициализация Frontend проекта

## Цель спринта

Создать полноценную инфраструктуру frontend приложения с выбранным технологическим стеком (Next.js + React + TypeScript + shadcn/ui + Tailwind CSS + pnpm), обеспечив базу для разработки дашборда и веб-чата.

## Выбранный технологический стек

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **UI Library**: shadcn/ui (компонентная библиотека)
- **Styling**: Tailwind CSS
- **Package Manager**: pnpm
- **Linting**: ESLint + Prettier
- **Type Checking**: TypeScript strict mode

## Этапы реализации

### 1. Создание документа Frontend Vision

**Файл**: `frontend/doc/frontend-vision.md`

По аналогии с `docs/vision.md` создать документ, описывающий:

- Концепцию frontend приложения (дашборд + веб-чат)
- Архитектурные принципы (компонентный подход, разделение concerns)
- Выбор технологий с обоснованием:
  - **Next.js 14+** - современный React фреймворк с App Router, SSR/SSG, отличная производительность
  - **TypeScript** - type safety, лучший DX, меньше багов
  - **shadcn/ui** - качественные компоненты, полный контроль, Radix UI primitives
  - **Tailwind CSS** - utility-first CSS, быстрая разработка, консистентный дизайн
  - **pnpm** - быстрый, эффективный пакетный менеджер
- Структура проекта (app/, components/, lib/, types/)
- Принципы разработки (KISS, реюзабельность, type safety)
- Интеграция с Backend API (Mock API → Real API)

### 2. Инициализация Next.js проекта

**Директория**: `frontend/app/`

```bash
# Из корня проекта
cd frontend
pnpm create next-app@latest app --typescript --tailwind --app --src-dir --import-alias "@/*"
```

Параметры инициализации:

- ✅ TypeScript
- ✅ ESLint
- ✅ Tailwind CSS
- ✅ App Router (не Pages Router)
- ✅ src/ directory
- ✅ Import alias (@/*)
- ❌ Turbopack (пока beta)

### 3. Настройка shadcn/ui

**Директория**: `frontend/app/`

```bash
cd app
pnpm dlx shadcn@latest init
```

Конфигурация:

- Style: Default
- Base color: Slate (подходит для темной темы)
- CSS variables: Yes

Установить базовые компоненты для дашборда:

```bash
pnpm dlx shadcn@latest add card button badge dropdown-menu tabs
```

Эти компоненты понадобятся для метрик, графиков, таблиц.

### 4. Настройка TypeScript конфигурации

**Файл**: `frontend/app/tsconfig.json`

Дополнить сгенерированный конфиг:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### 5. Настройка ESLint и Prettier

**Файл**: `frontend/app/.eslintrc.json`

Расширить стандартную конфигурацию Next.js:

```json
{
  "extends": [
    "next/core-web-vitals",
    "prettier"
  ],
  "rules": {
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "@typescript-eslint/no-unused-vars": ["error", {
      "argsIgnorePattern": "^_",
      "varsIgnorePattern": "^_"
    }]
  }
}
```

**Файл**: `frontend/app/.prettierrc`

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": false,
  "tabWidth": 2,
  "printWidth": 80
}
```

**Файл**: `frontend/app/.prettierignore`

```
.next
node_modules
pnpm-lock.yaml
```

### 6. Структура проекта

Создать базовую структуру директорий внутри `frontend/app/src/`:

```
frontend/app/src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout (темная тема)
│   ├── page.tsx           # Главная страница (redirect на /dashboard)
│   ├── dashboard/         # Дашборд статистики
│   │   └── page.tsx
│   └── chat/              # Веб-чат с AI
│       └── page.tsx
├── components/            # React компоненты
│   ├── ui/               # shadcn/ui компоненты (auto-generated)
│   ├── dashboard/        # Компоненты дашборда
│   └── chat/             # Компоненты чата
├── lib/                  # Утилиты и хелперы
│   ├── api.ts           # API клиент для Backend
│   └── utils.ts         # Общие утилиты (cn helper от shadcn)
└── types/               # TypeScript типы
    └── api.ts           # Типы для API контракта
```

### 7. Типизация API контракта

**Файл**: `frontend/app/src/types/api.ts`

На основе `frontend/doc/api-contract-example.json` создать TypeScript интерфейсы:

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
  timestamp: string;
  value: number;
}

export interface ConversationItem {
  conversation_id: number;
  user_id: number;
  messages_count: number;
  last_activity: string;
  created_at: string;
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

### 8. API клиент для Backend

**Файл**: `frontend/app/src/lib/api.ts`

```typescript
import { DashboardStats, Period } from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async getStats(period: Period): Promise<DashboardStats> {
    const response = await fetch(`${this.baseUrl}/api/stats?period=${period}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return response.json();
  }

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }
    return response.json();
  }
}

export const apiClient = new ApiClient();
```

### 9. Environment конфигурация

**Файл**: `frontend/app/.env.example`

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Файл**: `frontend/app/.env.local` (создать из .env.example)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Добавить в `.gitignore`:

```
.env.local
```

### 10. Root Layout с темной темой

**Файл**: `frontend/app/src/app/layout.tsx`

Настроить темную тему по умолчанию (как в референсе):

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AIDD Dashboard",
  description: "Statistics dashboard for AI Dialogue System",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

### 11. Placeholder страницы

**Файл**: `frontend/app/src/app/page.tsx`

```tsx
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/dashboard");
}
```

**Файл**: `frontend/app/src/app/dashboard/page.tsx`

```tsx
export default function DashboardPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="mt-4 text-muted-foreground">
          Coming in FE-SPRINT-3
        </p>
      </div>
    </div>
  );
}
```

**Файл**: `frontend/app/src/app/chat/page.tsx`

```tsx
export default function ChatPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold">AI Chat</h1>
        <p className="mt-4 text-muted-foreground">
          Coming in FE-SPRINT-4
        </p>
      </div>
    </div>
  );
}
```

### 12. Обновление Makefile

**Файл**: `Makefile` (корень проекта)

Добавить команды для frontend:

```makefile
# Frontend commands
.PHONY: fe-install fe-dev fe-build fe-lint fe-format fe-typecheck fe-quality

fe-install:
	cd frontend/app && pnpm install

fe-dev:
	cd frontend/app && pnpm dev

fe-build:
	cd frontend/app && pnpm build

fe-lint:
	cd frontend/app && pnpm lint

fe-format:
	cd frontend/app && pnpm format

fe-typecheck:
	cd frontend/app && pnpm typecheck

fe-quality: fe-format fe-lint fe-typecheck
	@echo "✅ Frontend quality checks passed"
```

### 13. Добавление scripts в package.json

**Файл**: `frontend/app/package.json`

Добавить дополнительные scripts:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit"
  }
}
```

### 14. Обновление README.md

**Файл**: `frontend/README.md`

Дополнить существующий README секциями:

- Quick Start для frontend разработки (установка pnpm, pnpm install)
- Команды запуска (make fe-dev, make fe-build, make fe-quality)
- Структура Next.js проекта
- Технологический стек с обоснованием выбора
- Конвенции разработки (TypeScript strict, компонентный подход)
- Ссылка на frontend-vision.md
- Примеры работы с API клиентом

### 15. Создание .gitignore для frontend

### 16. Сохранение плана спринта

**Файл**: `frontend/doc/plans/s2-frontend-init-plan.md`

Сохранить этот план в формате markdown для документирования спринта.

### 17. Добавление ссылки на план в roadmap

**Файл**: `frontend/doc/frontend-roadmap.md`

В таблице спринтов добавить ссылку на план в колонке "План" для FE-SPRINT-2:

```markdown
| **FE-SPRINT-2** | Каркас frontend проекта | 🚧 In Progress | [План](plans/s2-frontend-init-plan.md) |
```

### 18. Проверка всех package.json команд

Последовательно запустить и проверить все добавленные команды:

```bash
# Проверка каждой команды
pnpm dev      # Должен запуститься на localhost:3000
pnpm build    # Должен собраться без ошибок
pnpm lint     # Должен пройти без ошибок
pnpm format   # Должен отформатировать файлы
pnpm format:check  # Должен пройти проверку
pnpm typecheck     # TypeScript должен пройти без ошибок
```

### 19. Тестирование подключения к Mock API

Проверить интеграцию с Backend Mock API:

1. Запустить Backend API: `make api-dev` (в отдельном терминале)
2. Проверить health check: `curl http://localhost:8000/api/health`
3. Создать тестовый компонент или скрипт для проверки API клиента:

   - Вызов `apiClient.healthCheck()`
   - Вызов `apiClient.getStats("week")`

4. Убедиться что данные успешно получаются и соответствуют типам TypeScript
5. Проверить что CORS настроен корректно (запросы с localhost:3000 работают)

### 20. Финальная актуализация frontend-roadmap.md

**Файл**: `frontend/doc/frontend-roadmap.md`

После успешного завершения всех этапов обновить:

- Изменить статус FE-SPRINT-2 с "🚧 In Progress" на "✅ Completed"
- Добавить дату завершения
- Убедиться что ссылка на план присутствует
- Обновить версию документа и дату последнего обновления

**Файл**: `frontend/app/.gitignore`

```
# Dependencies
node_modules
.pnp
.pnp.js

# Next.js
.next
out
build
dist

# Environment
.env.local
.env.development.local
.env.test.local
.env.production.local

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Misc
.DS_Store
*.pem

# TypeScript
*.tsbuildinfo
next-env.d.ts
```

## Критерии успеха

- ✅ Next.js проект успешно инициализирован с TypeScript
- ✅ shadcn/ui установлен и базовые компоненты добавлены
- ✅ Dev сервер запускается на localhost:3000
- ✅ Темная тема применена (как в референсе)
- ✅ TypeScript strict mode без ошибок
- ✅ ESLint проходит без ошибок
- ✅ Prettier настроен и форматирование работает
- ✅ API типы созданы на основе контракта
- ✅ Структура проекта соответствует плану
- ✅ Makefile команды работают (fe-dev, fe-lint, fe-format, fe-typecheck)
- ✅ Документация актуализирована (frontend-vision.md, README.md)
- ✅ Placeholder страницы доступны (/dashboard, /chat)

## Файлы для создания/изменения

**Новые файлы**:

- `frontend/doc/frontend-vision.md`
- `frontend/app/` (весь Next.js проект)
- `frontend/app/src/types/api.ts`
- `frontend/app/src/lib/api.ts`
- `frontend/app/src/app/dashboard/page.tsx`
- `frontend/app/src/app/chat/page.tsx`
- `frontend/app/.env.example`
- `frontend/app/.env.local`
- `frontend/app/.prettierrc`
- `frontend/app/.prettierignore`

**Изменяемые файлы**:

- `Makefile` (добавить frontend команды)
- `frontend/README.md` (обновить с информацией о Next.js)
- `frontend/doc/frontend-roadmap.md` (обновить статус FE-SPRINT-2)
- `frontend/app/tsconfig.json` (дополнить strict настройками)
- `frontend/app/.eslintrc.json` (расширить правила)
- `frontend/app/package.json` (добавить scripts)

## Принципы разработки

- **Type Safety First**: строгая типизация везде
- **Component-Driven**: изолированные переиспользуемые компоненты
- **Dark Theme**: как в референсе дашборда
- **KISS**: простота и понятность кода
- **Quality Tools**: ESLint + Prettier + TypeScript для контроля качества
- **Documentation**: актуальная документация на каждом этапе

## Следующие шаги (FE-SPRINT-3)

После завершения инициализации можно будет приступить к реализации дашборда с интеграцией Mock API.

### To-dos

- [ ] Создать frontend-vision.md с концепцией и архитектурой
- [ ] Инициализировать Next.js проект с TypeScript и Tailwind
- [ ] Настроить shadcn/ui и установить базовые компоненты
- [ ] Настроить TypeScript strict mode
- [ ] Настроить ESLint и Prettier
- [ ] Создать структуру директорий (app/, components/, lib/, types/)
- [ ] Создать TypeScript типы для API контракта
- [ ] Реализовать API клиент для Backend
- [ ] Настроить environment конфигурацию (.env.example, .env.local)
- [ ] Настроить root layout с темной темой
- [ ] Создать placeholder страницы (/dashboard, /chat)
- [ ] Добавить frontend команды в Makefile
- [ ] Добавить дополнительные scripts в package.json
- [ ] Проверить все quality checks (lint, format, typecheck)
- [ ] Запустить dev сервер и проверить доступность страниц
- [ ] Обновить README.md и frontend-roadmap.md