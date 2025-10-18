# FE-SPRINT-4: Реализация ИИ-чата

## Цели

- Веб-интерфейс чата с floating button в dashboard
- Backend API для обработки чат-сообщений (аналог Telegram-бота)
- Два режима: обычный (LLM-ассистент) и admin (text2sql для статистики)
- Замена Mock API на Real API для статистики дашборда

## Архитектурные решения

### Frontend

- AIChatCard компонент из референса 21st.dev с адаптацией под проект
- Floating button (fixed position в правом нижнем углу dashboard)
- Session-based идентификация (случайный session_id в localStorage)
- Переключатель режимов (normal/admin) в header чата

### Backend Chat API

- Новые эндпоинты в `src/api/main.py`:
  - `POST /api/chat/message` - отправка сообщения
  - `POST /api/chat/clear` - очистка истории
  - `GET /api/chat/mode` - получение текущего режима
- Переиспользование `ConversationManager`, `LLMClient`, `DatabaseHistoryStorage`
- Session ID мапится на `user_id` в БД (используем hash для уникальности)

### Admin Mode (text2sql)

- Отдельный промпт для генерации SQL из естественного языка
- Pipeline:

  1. Вопрос пользователя → LLM генерирует SQL (только SELECT)
  2. Валидация SQL (проверка на безопасность)
  3. Выполнение SQL запроса к БД
  4. Результат → LLM форматирует ответ на естественном языке

- Доступ только к таблицам: conversations, user_messages, llm_responses

### Real Stat Collector

- `RealStatCollector` класс реализует интерфейс `StatCollector`
- SQL запросы к реальной БД для всех метрик
- Переключение через dependency injection в `src/api/main.py`

## Реализация

### 1. Backend: Chat API эндпоинты

**Файл: `src/api/main.py`**

Добавить:

```python
from pydantic import BaseModel

class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    mode: str = "normal"  # "normal" or "admin"

class ChatMessageResponse(BaseModel):
    response: str
    mode: str
    sql_query: str | None = None  # для admin mode

@app.post("/api/chat/message")
async def send_message(request: ChatMessageRequest) -> ChatMessageResponse:
    # Конвертируем session_id в user_id (hash)
    user_id = hash(request.session_id) % (10**9)

    # Выбираем ConversationManager в зависимости от режима
    if request.mode == "admin":
        response, sql = await admin_conversation_manager.process_message_with_sql(user_id, request.message)
        return ChatMessageResponse(response=response, mode="admin", sql_query=sql)
    else:
        response = await normal_conversation_manager.process_message(user_id, request.message)
        return ChatMessageResponse(response=response, mode="normal")

@app.post("/api/chat/clear")
async def clear_history(session_id: str):
    user_id = hash(session_id) % (10**9)
    await normal_conversation_manager.clear_history(user_id)
    await admin_conversation_manager.clear_history(user_id)
    return {"status": "cleared"}
```

Инициализация:

- Создать два `ConversationManager`: `normal_conversation_manager` и `admin_conversation_manager`
- Normal: использует существующий system prompt
- Admin: использует специальный text2sql prompt

### 2. Backend: Admin Mode - Text2SQL Manager

**Файл: `src/api/text2sql_manager.py`** (новый)

```python
class Text2SQLManager:
    """Менеджер для обработки запросов в admin режиме с text2sql"""

    def __init__(self, llm_client: LLMClient, engine: AsyncEngine):
        self.llm_client = llm_client
        self.engine = engine
        self.text2sql_prompt = self._load_text2sql_prompt()

    async def process_query(self, user_id: int, question: str) -> tuple[str, str]:
        """
        Pipeline: question → SQL → execute → format answer
        Returns: (answer, sql_query)
        """
        # 1. Генерация SQL из вопроса
        sql_query = await self._generate_sql(question)

        # 2. Валидация SQL
        if not self._is_safe_sql(sql_query):
            return ("Извините, запрос не может быть выполнен по соображениям безопасности.", sql_query)

        # 3. Выполнение SQL
        result = await self._execute_sql(sql_query)

        # 4. Форматирование ответа через LLM
        answer = await self._format_answer(question, result)

        return (answer, sql_query)
```

Text2SQL промпт должен включать:

- Схему таблиц БД (conversations, user_messages, llm_responses)
- Примеры вопросов и SQL запросов
- Инструкции генерировать только SELECT запросы

### 3. Backend: RealStatCollector

**Файл: `src/api/real_stat_collector.py`** (новый)

```python
class RealStatCollector(StatCollector):
    """Реальный сборщик статистики из БД"""

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def get_stats(self, period: str) -> DashboardStats:
        # SQL запросы для:
        # 1. Total Conversations за period
        # 2. New Users за period
        # 3. Active Conversations за period
        # 4. Avg Messages per Conversation
        # 5. Activity chart (timeseries)
        # 6. Recent 10 conversations
        # 7. Top 5 users
```

Примеры SQL:

- Total Conversations: `SELECT COUNT(*) FROM conversations WHERE created_at >= ?`
- Activity chart: `SELECT DATE_TRUNC('hour', timestamp), COUNT(*) FROM user_messages GROUP BY ...`

**Файл: `src/api/main.py`**

Заменить:

```python
# Было
collector = MockStatCollector()

# Стало
from .real_stat_collector import RealStatCollector
collector = RealStatCollector(engine)
```

### 4. Frontend: AI Chat компонент

**Файл: `frontend/app/src/components/chat/AIChatCard.tsx`** (новый)

Адаптировать референс из 21st.dev:

- Добавить props: `mode` ("normal" | "admin"), `onModeChange`
- Интегрировать с API (`/api/chat/message`, `/api/chat/clear`)
- Session ID генерация и хранение в localStorage
- Отображение SQL запроса в admin режиме (collapsible)

**Файл: `frontend/app/src/components/chat/ChatToggle.tsx`** (новый)

Toggle компонент для переключения режимов:

```tsx
<Switch checked={mode === "admin"} onCheckedChange={...} />
<Label>Admin Mode (Analytics)</Label>
```

**Файл: `frontend/app/src/components/chat/FloatingChatButton.tsx`** (новый)

Floating button в правом нижнем углу:

```tsx
<button className="fixed bottom-6 right-6 z-50">
  {isOpen ? <X /> : <MessageCircle />}
</button>
{isOpen && <AIChatCard ... />}
```

### 5. Frontend: Интеграция в Dashboard

**Файл: `frontend/app/src/app/dashboard/page.tsx`**

Добавить:

```tsx
import { FloatingChatButton } from "@/components/chat/FloatingChatButton";

export default function DashboardPage() {
  return (
    <div>
      {/* existing content */}
      <FloatingChatButton />
    </div>
  );
}
```

### 6. Frontend: API типы и клиент

**Файл: `frontend/app/src/types/api.ts`**

Добавить:

```typescript
export interface ChatMessage {
  session_id: string;
  message: string;
  mode: "normal" | "admin";
}

export interface ChatResponse {
  response: string;
  mode: string;
  sql_query?: string;
}
```

**Файл: `frontend/app/src/lib/api.ts`**

Добавить методы:

```typescript
async sendChatMessage(request: ChatMessage): Promise<ChatResponse>
async clearChatHistory(sessionId: string): Promise<void>
```

### 7. Backend: Text2SQL промпт

**Файл: `prompts/system_prompt_text2sql.txt`** (новый)

Содержание:

- Роль: SQL Generator для аналитики диалогов
- Схема БД с описанием таблиц
- Примеры вопросов и SQL
- Правила безопасности (только SELECT)

### 8. Зависимости

**Frontend:**

```bash
cd frontend/app
pnpm add framer-motion lucide-react
```

Компоненты shadcn/ui:

```bash
pnpm dlx shadcn@latest add switch label dialog
```

**Backend:**

Уже установлены: fastapi, sqlalchemy, asyncpg

### 9. Конфигурация

**.env файл** - добавить опциональные переменные:

```
# Chat settings
CHAT_MAX_HISTORY=10
ENABLE_ADMIN_MODE=true
```

### 10. Тестирование

- Backend API: curl тесты для `/api/chat/message`, `/api/chat/clear`
- Frontend: manual testing чат-интерфейса
- Real stat collector: проверка SQL запросов и данных
- Admin mode: тестирование text2sql запросов

## Структура файлов

### Backend (новые)

- `src/api/text2sql_manager.py` - Text2SQL pipeline
- `src/api/real_stat_collector.py` - Реальный сборщик статистики
- `prompts/system_prompt_text2sql.txt` - Промпт для text2sql

### Backend (изменения)

- `src/api/main.py` - Chat эндпоинты + переключение на RealStatCollector

### Frontend (новые)

- `frontend/app/src/components/chat/AIChatCard.tsx` - Компонент чата
- `frontend/app/src/components/chat/FloatingChatButton.tsx` - Floating button
- `frontend/app/src/components/chat/ChatToggle.tsx` - Переключатель режимов
- `frontend/app/src/components/ui/switch.tsx` - Switch компонент (shadcn)
- `frontend/app/src/components/ui/label.tsx` - Label компонент (shadcn)

### Frontend (изменения)

- `frontend/app/src/app/dashboard/page.tsx` - Интеграция FloatingChatButton
- `frontend/app/src/lib/api.ts` - Chat методы
- `frontend/app/src/types/api.ts` - Chat типы

## Порядок выполнения

1. Backend: RealStatCollector (замена Mock на Real для дашборда)
2. Backend: Text2SQL промпт и Text2SQLManager
3. Backend: Chat API эндпоинты с normal + admin режимами
4. Frontend: Установка зависимостей (framer-motion, shadcn компоненты)
5. Frontend: AIChatCard компонент (адаптация референса)
6. Frontend: FloatingChatButton и интеграция в dashboard
7. Frontend: API клиент для чата
8. Тестирование: проверка всех режимов и функциональности
9. Качество: ESLint, Prettier, TypeScript, ruff, mypy

## Ожидаемый результат

- ✅ Floating chat button в dashboard (правый нижний угол)
- ✅ Раскрывающийся чат с анимациями (референс 21st.dev)
- ✅ Два режима: Normal (LLM-ассистент) и Admin (аналитика)
- ✅ Backend Chat API с интеграцией ConversationManager
- ✅ Text2SQL pipeline для admin режима
- ✅ Real статистика дашборда (замена Mock на Real)
- ✅ История чата сохраняется в БД
- ✅ Session-based идентификация пользователей
- ✅ Качественный код (0 ошибок линтеров, тайпчекеров)
