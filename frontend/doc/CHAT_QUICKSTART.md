# Chat Quick Start Guide

Быстрый старт для работы с ИИ-чатом в dashboard.

## Запуск системы

### 1. Backend API

```bash
# Из корневой директории проекта
python -m src.api_server
```

API будет доступен на http://localhost:8000

**Swagger UI:** http://localhost:8000/docs

### 2. Frontend Dev Server

```bash
cd frontend/app
pnpm dev
```

Frontend будет доступен на http://localhost:3000

## Использование чата

### Открытие чата

1. Откройте http://localhost:3000/dashboard
2. В правом нижнем углу будет floating button с иконкой сообщения
3. Кликните на кнопку чтобы открыть чат

### Normal Mode (по умолчанию)

Обычный режим LLM-ассистента:

**Примеры вопросов:**
- "Расскажи о себе"
- "Как мне улучшить производительность Python?"
- "Объясни что такое async/await"

### Admin Mode

Режим аналитики диалогов через text2sql:

1. Переключите toggle "Admin Mode (Analytics)"
2. Задавайте вопросы о статистике

**Примеры вопросов:**
- "Сколько всего диалогов в системе?"
- "Покажи топ 5 самых активных пользователей"
- "Какая средняя длина сообщений пользователей?"
- "Сколько новых пользователей появилось за последнюю неделю?"
- "Покажи последние 10 диалогов"

### SQL Queries

В admin режиме:
- SQL запросы отображаются под ответом AI
- Можно скопировать SQL для дальнейшего использования
- SQL генерируется автоматически через LLM

### Очистка истории

Кликните на иконку корзины в header чата для очистки истории диалога.

## Конфигурация

### Environment Variables

Создайте `.env` файл в корне проекта:

```env
# Обязательные
TELEGRAM_BOT_TOKEN=your_token_here
OPENROUTER_API_KEY=your_api_key_here

# Опциональные
DEFAULT_MODEL=openai/gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7
MAX_HISTORY_MESSAGES=10

# Выбор между Mock и Real статистикой
USE_MOCK_STATS=false  # false = Real, true = Mock

# База данных
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

### Mock vs Real Statistics

- **Real (default)**: использует реальную БД для статистики
- **Mock**: генерирует тестовые данные (если БД недоступна)

Переключение через `USE_MOCK_STATS=true` в `.env`

## API Endpoints

### Chat Endpoints

#### POST /api/chat/message
Отправка сообщения в чат.

**Request:**
```json
{
  "session_id": "uuid-string",
  "message": "Your question here",
  "mode": "normal"  // or "admin"
}
```

**Response:**
```json
{
  "response": "AI assistant answer",
  "mode": "normal",
  "sql_query": null  // only in admin mode
}
```

#### POST /api/chat/clear
Очистка истории диалога.

**Request:**
```json
{
  "session_id": "uuid-string"
}
```

**Response:**
```json
{
  "status": "cleared",
  "session_id": "uuid-string"
}
```

### Statistics Endpoints

#### GET /api/stats?period=week
Получение статистики дашборда.

**Query Parameters:**
- `period`: `day` | `week` | `month`

## Troubleshooting

### Backend не запускается

1. Проверьте что установлены все зависимости:
   ```bash
   uv sync
   ```

2. Проверьте `.env` файл (обязательны `TELEGRAM_BOT_TOKEN` и `OPENROUTER_API_KEY`)

3. Если БД недоступна, используйте Mock статистику:
   ```bash
   USE_MOCK_STATS=true python -m src.api_server
   ```

### Frontend не подключается к API

1. Проверьте что Backend запущен на порту 8000
2. Проверьте переменную окружения:
   ```bash
   # frontend/app/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Chat не отвечает

1. Проверьте консоль браузера (F12) на ошибки
2. Проверьте что у вас есть валидный `OPENROUTER_API_KEY`
3. Проверьте логи backend в терминале

### TypeScript ошибки

Игнорируйте ошибки в `MatrixBackground.tsx` - они не влияют на функциональность чата.

Для проверки только chat компонентов:
```bash
cd frontend/app
pnpm typecheck
```

## Архитектура

### Session Management

- Session ID генерируется автоматически (UUID)
- Хранится в `localStorage` браузера
- Backend конвертирует session_id → user_id через hash
- История сохраняется в БД

### Text2SQL Pipeline

1. User Question → LLM (с text2sql промптом)
2. LLM генерирует SQL запрос
3. SQL валидируется (только SELECT, безопасность)
4. SQL выполняется на БД
5. Результат → LLM (форматирование ответа)
6. Ответ отображается в UI
7. SQL показывается в collapsible блоке

## Дополнительная информация

- **План спринта:** [s4-chat-plan.md](plans/s4-chat-plan.md)
- **Отчет о завершении:** [sprint-4-completion-report.md](sprint-4-completion-report.md)
- **Roadmap:** [frontend-roadmap.md](frontend-roadmap.md)

## Известные ограничения

1. Text2SQL поддерживает только SELECT запросы
2. Доступ только к таблицам: conversations, user_messages, llm_responses
3. Session не персистится между устройствами (local storage)
4. Нет streaming ответов (будет в будущих версиях)

## Следующие шаги

После тестирования чата:
1. Настройте production БД
2. Обновите environment variables для production
3. Тестируйте text2sql запросы на реальных данных
4. Настройте мониторинг API
