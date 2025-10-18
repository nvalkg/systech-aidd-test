# Примеры запросов к Statistics API

## Обзор

Этот документ содержит примеры использования Statistics API для тестирования и разработки frontend.

## Базовая информация

- **Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Эндпоинты

### 1. Health Check

Проверка доступности API.

**Запрос:**

```bash
curl http://localhost:8000/api/health
```

**Ответ:**

```json
{
  "status": "ok"
}
```

### 2. Получить статистику за день

**Запрос:**

```bash
curl "http://localhost:8000/api/stats?period=day"
```

**С форматированием:**

```bash
curl "http://localhost:8000/api/stats?period=day" | python -m json.tool
```

**Ожидаемый ответ:** JSON со статистикой за последние 24 часа (24 точки на графике активности)

### 3. Получить статистику за неделю

**Запрос:**

```bash
curl "http://localhost:8000/api/stats?period=week"
```

**Ожидаемый ответ:** JSON со статистикой за последние 7 дней (7 точек на графике активности)

### 4. Получить статистику за месяц

**Запрос:**

```bash
curl "http://localhost:8000/api/stats?period=month"
```

**Ожидаемый ответ:** JSON со статистикой за последние 30 дней (30 точек на графике активности)

### 5. Некорректный запрос

**Запрос:**

```bash
curl "http://localhost:8000/api/stats?period=year"
```

**Ответ:**

```json
{
  "detail": "Invalid period: year. Must be 'day', 'week', or 'month'"
}
```

**HTTP Status:** 400 Bad Request

## Примеры на JavaScript

### Fetch API

```javascript
// Получить статистику за неделю
async function getWeeklyStats() {
  try {
    const response = await fetch('http://localhost:8000/api/stats?period=week');

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Stats:', data);
    return data;
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
}

// Использование
getWeeklyStats().then(stats => {
  console.log('Total Conversations:', stats.metrics[0].value);
  console.log('Activity Chart Points:', stats.activity_chart.length);
});
```

### Axios

```javascript
import axios from 'axios';

// Получить статистику за день
async function getDailyStats() {
  try {
    const response = await axios.get('http://localhost:8000/api/stats', {
      params: { period: 'day' }
    });

    console.log('Stats:', response.data);
    return response.data;
  } catch (error) {
    if (error.response) {
      // Ошибка от сервера
      console.error('Error:', error.response.status, error.response.data);
    } else {
      console.error('Error:', error.message);
    }
  }
}
```

### React Hook

```javascript
import { useState, useEffect } from 'react';

function useDashboardStats(period = 'week') {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStats() {
      try {
        setLoading(true);
        const response = await fetch(
          `http://localhost:8000/api/stats?period=${period}`
        );

        if (!response.ok) {
          throw new Error('Failed to fetch stats');
        }

        const data = await response.json();
        setStats(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, [period]);

  return { stats, loading, error };
}

// Использование в компоненте
function Dashboard() {
  const { stats, loading, error } = useDashboardStats('week');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!stats) return null;

  return (
    <div>
      <h1>Dashboard</h1>
      {stats.metrics.map((metric, index) => (
        <div key={index}>
          <h2>{metric.title}</h2>
          <p>{metric.value}</p>
          <p>Trend: {metric.trend}%</p>
        </div>
      ))}
    </div>
  );
}
```

## Тестирование с разными периодами

```bash
# Последовательное тестирование всех периодов
echo "=== Testing DAY period ==="
curl -s "http://localhost:8000/api/stats?period=day" | python -m json.tool | head -n 20

echo "\n=== Testing WEEK period ==="
curl -s "http://localhost:8000/api/stats?period=week" | python -m json.tool | head -n 20

echo "\n=== Testing MONTH period ==="
curl -s "http://localhost:8000/api/stats?period=month" | python -m json.tool | head -n 20
```

## Структура ответа

### Полный пример ответа

См. файл `frontend/doc/api-contract-example.json` для полного примера структуры ответа.

### Краткое описание полей

```json
{
  "metrics": [
    // 4 карточки метрик
    {
      "title": "Название метрики",
      "value": "Значение (строка)",
      "trend": 12.5,  // число (может быть отрицательным)
      "trend_label": "Описание тренда",
      "description": "Дополнительное описание"
    }
  ],
  "activity_chart": [
    // Массив точек для графика
    {
      "timestamp": "2025-10-17T14:00:00Z",  // ISO 8601
      "value": 142  // число
    }
  ],
  "recent_conversations": [
    // Последние 10 диалогов
    {
      "conversation_id": 1523,
      "user_id": 987654321,
      "messages_count": 8,
      "last_activity": "2025-10-17T14:35:22Z",
      "created_at": "2025-10-17T10:15:00Z"
    }
  ],
  "top_users": [
    // Топ 5 пользователей
    {
      "user_id": 123456789,
      "messages_count": 245,
      "conversations_count": 12
    }
  ],
  "period": "week"  // выбранный период
}
```

## Запуск API сервера

### Вариант 1: Через make (рекомендуется)

```bash
# Запуск в режиме разработки с auto-reload
make api-dev

# Или просто запуск
make api-run
```

### Вариант 2: Напрямую через uvicorn

```bash
# С auto-reload
uv run uvicorn src.api.main:app --reload --port 8000

# Без auto-reload
uv run uvicorn src.api.main:app --port 8000
```

### Вариант 3: Через Python модуль

```bash
uv run python -m src.api_server
```

## Проверка работоспособности

После запуска сервера выполните:

```bash
# 1. Проверка health check
curl http://localhost:8000/api/health

# 2. Проверка основного эндпоинта
make api-test

# 3. Открыть Swagger UI в браузере
# http://localhost:8000/docs
```

## CORS

API настроен с разрешением CORS для всех origins (`allow_origins=["*"]`), что позволяет делать запросы с любого домена во время разработки.

**Важно:** В production окружении следует ограничить `allow_origins` конкретными доменами frontend приложения.

## Troubleshooting

### Проблема: Port already in use

```bash
# Найти процесс на порту 8000
lsof -i :8000

# Завершить процесс
kill -9 <PID>
```

### Проблема: Module not found

```bash
# Установить/обновить зависимости
uv sync
```

### Проблема: CORS errors в браузере

Убедитесь, что API сервер запущен и настроен с CORS middleware (уже настроено в `src/api/main.py`).
