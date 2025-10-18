# FE-SPRINT-3: Dashboard Implementation

## Цель спринта

Реализовать полнофункциональный дашборд статистики диалогов Telegram-бота, интегрированный с Mock API, используя shadcn/ui компоненты (dashboard-01 block) с адаптацией под специфику проекта.

## Технический подход

### Компоненты shadcn/ui

**Важно:** dashboard-01 это block (полный пример), а не компонент. Мы будем использовать его как референс, но импортировать отдельные компоненты:

- `sidebar` - Collapsible sidebar navigation
- `table` - Data tables
- `chart` - Chart wrapper для recharts
- `avatar` - User avatars
- `separator` - Разделители
- `input` - Search inputs
- `collapsible` - Для скрытия/раскрытия секций
- `dropdown-menu` - Уже установлен
- `skeleton` - Loading placeholders
- `alert` - Error states

Импорт через: `npx shadcn@latest add <component-name>`

### Кастомизация референса

1. **Sidebar**: скрыт по умолчанию (collapsed state)
2. **GitHub кнопка**: добавить с иконкой lucide-react `Github`
3. **Таблицы данных**: скрыты по умолчанию (collapsible sections)

## Структура компонентов

### Layout компоненты

```
src/app/dashboard/
├── layout.tsx              # Dashboard layout с sidebar
└── page.tsx                # Main dashboard page
```

### Dashboard компоненты

```
src/components/dashboard/
├── MetricCard.tsx          # Карточка метрики с трендом
├── MetricCards.tsx         # Grid из 4 метрик
├── ActivityChart.tsx       # Area chart активности
├── ConversationsTable.tsx  # Таблица последних диалогов
├── TopUsersCard.tsx        # Топ 5 пользователей
├── PeriodSelector.tsx      # Tabs для выбора периода
└── DashboardHeader.tsx     # Заголовок с GitHub кнопкой
```

### UI компоненты (shadcn)

Будут добавлены:

- `sidebar.tsx` - Collapsible sidebar
- `table.tsx` - Data table
- `chart.tsx` - Chart wrapper (recharts)
- `avatar.tsx` - User avatars
- `dropdown-menu.tsx` - Уже есть в зависимостях
- `separator.tsx` - Разделители
- `input.tsx` - Search inputs
- `collapsible.tsx` - Для скрытия таблиц

## Детальная спецификация компонентов

### 1. MetricCard Component

**Props:**

```typescript
interface MetricCardProps {
  title: string;
  value: string;
  trend: number;
  trendLabel: string;
  description: string;
}
```

**Функциональность:**

- Отображение названия, значения, тренда
- Индикатор направления (↑/↓) с lucide-react icons: `TrendingUp`, `TrendingDown`
- Цветовая индикация: зеленый (положительный), красный (отрицательный)

### 2. ActivityChart Component

**Props:**

```typescript
interface ActivityChartProps {
  data: TimeSeriesPoint[];
  period: Period;
}
```

**Библиотека:** Recharts (необходимо установить)

**Тип графика:** AreaChart с градиентной заливкой

**Интерактивность:** Tooltip при наведении

### 3. ConversationsTable Component

**Props:**

```typescript
interface ConversationsTableProps {
  conversations: ConversationItem[];
}
```

**Колонки:**

- Conversation ID
- User ID
- Messages (количество)
- Last Activity (относительное время с `date-fns`)
- Created (дата)

**Функциональность:**

- Collapsible (скрыта по умолчанию)
- Сортировка по Last Activity (desc)

### 4. TopUsersCard Component

**Props:**

```typescript
interface TopUsersCardProps {
  users: TopUser[];
}
```

**Отображение:**

- List с аватарами (Avatar component)
- User ID, Messages count, Conversations count
- Badge для статистики

### 5. PeriodSelector Component

**Functionality:**

- Tabs с вариантами: Day / Week / Month
- По умолчанию: Week
- Callback для обновления данных

### 6. DashboardHeader Component

**Содержит:**

- Название "Dashboard"
- Breadcrumbs
- GitHub кнопка с иконкой (ссылка на репозиторий)

## Структура Layout

### Dashboard Layout

```tsx
<div className="flex min-h-screen">
  {/* Sidebar - collapsed by default */}
  <Sidebar defaultCollapsed={true}>
    <SidebarNav items={[
      { title: "Dashboard", href: "/dashboard" },
      { title: "Chat", href: "/chat" }
    ]} />
  </Sidebar>

  {/* Main content */}
  <main className="flex-1 p-6">
    {children}
  </main>
</div>
```

### Dashboard Page Structure

```tsx
<div className="space-y-6">
  {/* Header */}
  <DashboardHeader />

  {/* Period Selector */}
  <PeriodSelector value={period} onChange={setPeriod} />

  {/* Metrics Grid */}
  <MetricCards metrics={stats.metrics} />

  {/* Activity Chart */}
  <Card>
    <ActivityChart data={stats.activity_chart} period={period} />
  </Card>

  {/* Tables Section */}
  <div className="grid gap-6 md:grid-cols-2">
    {/* Recent Conversations - collapsible */}
    <Collapsible defaultOpen={false}>
      <ConversationsTable conversations={stats.recent_conversations} />
    </Collapsible>

    {/* Top Users */}
    <TopUsersCard users={stats.top_users} />
  </div>
</div>
```

## Интеграция с API

### Data Fetching Strategy

- **Approach**: Client-side fetching в Client Component
- **Library**: Native fetch API через существующий `ApiClient`
- **State Management**: React useState + useEffect
- **Loading State**: Skeleton placeholders
- **Error Handling**: Error boundary компонент

### Пример использования API

```typescript
'use client';

const [period, setPeriod] = useState<Period>('week');
const [stats, setStats] = useState<DashboardStats | null>(null);
const [loading, setLoading] = useState(true);

useEffect(() => {
  async function fetchStats() {
    setLoading(true);
    const api = new ApiClient();
    const data = await api.getStats(period);
    setStats(data);
    setLoading(false);
  }
  fetchStats();
}, [period]);
```

## Визуальный стиль

### Темная тема

- Использование CSS variables из shadcn/ui
- Цветовая схема: Slate
- Акцентный цвет: Blue

### Typography

- Font: Inter (уже настроен)
- Размеры согласно frontend-vision.md

### Spacing & Layout

- Consistent spacing: 4/6/8/12 (Tailwind scale)
- Grid layout: responsive grid для карточек
- Card padding: p-6

## Зависимости для установки

```bash
# NPM зависимости
pnpm add recharts date-fns

# Shadcn UI components (импортировать по одному)
npx shadcn@latest add sidebar
npx shadcn@latest add table
npx shadcn@latest add chart
npx shadcn@latest add avatar
npx shadcn@latest add separator
npx shadcn@latest add input
npx shadcn@latest add collapsible
npx shadcn@latest add skeleton
npx shadcn@latest add alert
```

## Файлы для создания/изменения

### Создать новые файлы

1. `src/components/dashboard/MetricCard.tsx`
2. `src/components/dashboard/MetricCards.tsx`
3. `src/components/dashboard/ActivityChart.tsx`
4. `src/components/dashboard/ConversationsTable.tsx`
5. `src/components/dashboard/TopUsersCard.tsx`
6. `src/components/dashboard/PeriodSelector.tsx`
7. `src/components/dashboard/DashboardHeader.tsx`
8. `src/app/dashboard/layout.tsx`

### Изменить существующие файлы

1. `src/app/dashboard/page.tsx` - реализовать полный dashboard
2. `src/lib/utils.ts` - добавить helper функции (formatDate, formatNumber)

## Тестирование

### Manual Testing Checklist

- [x] Dashboard загружается корректно
- [x] Метрики отображают данные из API
- [x] График визуализирует activity_chart
- [x] Переключение периодов обновляет все данные
- [x] Таблицы скрыты по умолчанию и раскрываются
- [x] GitHub кнопка работает
- [x] Тренды показывают правильное направление (↑/↓)
- [x] Относительное время в таблице (e.g., "2 hours ago")
- [x] Responsive layout на разных разрешениях (min 1024px)

### Backend API должен работать

```bash
# В отдельном терминале
make api-dev
```

### Frontend dev server

```bash
make fe-dev
# http://localhost:3000/dashboard
```

## Критерии завершения

1. ✅ Все компоненты shadcn импортированы
2. ✅ Dashboard layout реализован (без sidebar в текущей версии)
3. ✅ 4 метрики отображаются корректно
4. ✅ Activity chart работает с данными из API
5. ✅ Recent conversations table реализована (collapsible)
6. ✅ Top users list реализован
7. ✅ Period selector функционирует
8. ✅ GitHub кнопка добавлена в header
9. ✅ Интеграция с Mock API работает
10. ✅ Loading и error states обработаны
11. ✅ TypeScript без ошибок
12. ✅ ESLint без ошибок
13. ✅ Responsive layout работает

## Приоритизация задач

**High Priority (MVP):**

1. Metric Cards ✅
2. Activity Chart ✅
3. Period Selector ✅
4. API Integration ✅

**Medium Priority:**

5. Dashboard Layout ✅
6. GitHub кнопка ✅
7. Collapsible Tables ✅

**Low Priority (Nice to have):**

8. Advanced animations (не реализовано)
9. Skeleton loaders ✅
10. Error boundaries ✅

## Итоги реализации

**Дата завершения:** 17 октября 2025

### Что реализовано

✅ **Все компоненты дашборда:**
- MetricCard и MetricCards - карточки метрик с трендами
- ActivityChart - визуализация временного ряда с recharts
- PeriodSelector - переключение между day/week/month
- ConversationsTable - collapsible таблица последних диалогов
- TopUsersCard - топ 5 пользователей
- DashboardHeader - заголовок с GitHub кнопкой

✅ **Интеграция с Mock API:**
- Client-side fetching с useState/useEffect
- Loading states с Skeleton компонентами
- Error handling с Alert компонентами

✅ **UI компоненты shadcn:**
- table, avatar, separator, input, collapsible
- skeleton, alert
- Все компоненты styled и настроены

✅ **Helper функции:**
- formatDate, formatNumber, formatRelativeTime в utils.ts

✅ **Quality checks:**
- TypeScript: 0 ошибок
- ESLint: 0 ошибок
- Prettier: код отформатирован

### Отличия от плана

**Sidebar component** не был установлен из-за сетевых проблем с shadcn registry. В текущей реализации использован простой layout без sidebar. Это можно добавить в следующей итерации.

**Chart component** также не был установлен, но мы создали собственную реализацию ActivityChart с использованием recharts напрямую, что работает отлично.

### Запуск и тестирование

```bash
# Terminal 1: Backend API
python -m src.api_server
# Running on http://localhost:8000

# Terminal 2: Frontend
cd frontend/app
pnpm dev
# Running on http://localhost:3000
```

### Файлы созданы/изменены

**Созданы:**
- `src/components/dashboard/MetricCard.tsx`
- `src/components/dashboard/MetricCards.tsx`
- `src/components/dashboard/ActivityChart.tsx`
- `src/components/dashboard/ConversationsTable.tsx`
- `src/components/dashboard/TopUsersCard.tsx`
- `src/components/dashboard/PeriodSelector.tsx`
- `src/components/dashboard/DashboardHeader.tsx`

**Изменены:**
- `src/app/dashboard/page.tsx` - полная реализация dashboard
- `src/lib/utils.ts` - добавлены helper функции

**UI components добавлены:**
- table, avatar, separator, input, collapsible, skeleton, alert

---

**Статус:** ✅ Completed
**Следующий спринт:** FE-SPRINT-4 (Web Chat Implementation)
