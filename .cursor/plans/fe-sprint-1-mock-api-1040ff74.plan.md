<!-- 1040ff74-fe41-43b6-a0e1-14c3554eab8c b9026002-851a-425a-bd01-f5fd1eab1d02 -->
# FE-SPRINT-1: Mock API для дашборда статистики

## Обзор

Создать Mock API для дашборда статистики диалогов с полной документацией, позволяющей начать независимую разработку frontend. API будет основан на FastAPI с автоматической генерацией Swagger документации.

## Анализ референса и структуры БД

**Референс дашборда** (`frontend/doc/frontend-reference.jpg`) содержит:

- 4 карточки метрик с трендами (Total Revenue, New Customers, Active Accounts, Growth Rate)
- График временных рядов (Total Visitors) с фильтрацией по периодам (3 months, 30 days, 7 days)

**Адаптация метрик под контекст диалогов**:

- Total Revenue → **Total Conversations** (всего диалогов)
- New Customers → **New Users** (новых пользователей за период)
- Active Accounts → **Active Conversations** (активных диалогов за период)
- Growth Rate → **Average Messages per Conversation** (среднее сообщений на диалог)
- Total Visitors → **Message Activity** (график активности сообщений)

**Структура БД** (из `src/database.py`):

- `conversations`: id, user_id, system_prompt, created_at, updated_at
- `user_messages`: id, conversation_id, user_id, text, content_length, timestamp, is_deleted
- `llm_responses`: id, conversation_id, content, content_length, model_used, timestamp, is_deleted

## Этапы реализации

### 1. Документ функциональных требований

**Файл**: `frontend/doc/dashboard-requirements.md`

Содержит:

- Описание метрик дашборда (4 карточки + график)
- Адаптация метрик из референса под контекст Telegram-бота
- Требования к фильтрации (day/week/month)
- Описание структуры данных для каждого виджета
- Примеры UI/UX взаимодействий

### 2. API контракт и модели данных

**Файл**: `src/api/models.py`

Создать dataclasses для API контракта:

```python
@dataclass
class MetricCard:
    """Карточка метрики"""
    title: str
    value: str
    trend: float  # процент изменения, может быть отрицательным
    trend_label: str
    description: str

@dataclass
class TimeSeriesPoint:
    """Точка временного ряда"""
    timestamp: str  # ISO format
    value: int

@dataclass
class ConversationItem:
    """Элемент списка диалогов"""
    conversation_id: int
    user_id: int
    messages_count: int
    last_activity: str  # ISO format
    created_at: str  # ISO format

@dataclass
class TopUser:
    """Пользователь в топе активности"""
    user_id: int
    messages_count: int
    conversations_count: int

@dataclass
class DashboardStats:
    """Полная статистика для дашборда"""
    metrics: list[MetricCard]  # 4 карточки
    activity_chart: list[TimeSeriesPoint]  # данные графика
    recent_conversations: list[ConversationItem]  # последние 10 диалогов
    top_users: list[TopUser]  # топ 5 пользователей
    period: str  # выбранный период
```

**Файл**: `frontend/doc/api-contract-example.json`

Создать полный пример JSON ответа API с реалистичными данными для всех периодов (day/week/month).

### 3. Интерфейс StatCollector

**Файл**: `src/api/stat_collector.py`

```python
from abc import ABC, abstractmethod
from .models import DashboardStats

class StatCollector(ABC):
    """Интерфейс для сборщика статистики"""
    
    @abstractmethod
    async def get_stats(self, period: str) -> DashboardStats:
        """
        Получить статистику за период
        
        Args:
            period: Период ('day', 'week', 'month')
            
        Returns:
            Статистика для дашборда
        """
        pass
```

### 4. Mock реализация

**Файл**: `src/api/mock_stat_collector.py`

Реализовать `MockStatCollector(StatCollector)` с:

- Генерацией реалистичных данных для трех периодов (day/week/month)
- Вариативностью данных при каждом запросе (random seed для консистентности)
- Соблюдением бизнес-логики (новые пользователи <= активные диалоги)
- Генерацией временных рядов с правдоподобными паттернами
- Списком из 10 последних диалогов с разными user_id
- Топ 5 пользователей по активности

### 5. FastAPI приложение

**Файл**: `src/api/main.py`

```python
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .mock_stat_collector import MockStatCollector

app = FastAPI(
    title="AIDD Statistics API",
    description="API для получения статистики по диалогам Telegram-бота",
    version="1.0.0"
)

# CORS для frontend разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

collector = MockStatCollector()

@app.get("/api/stats")
async def get_stats(
    period: str = Query("week", regex="^(day|week|month)$")
):
    """Получить статистику за период"""
    stats = await collector.get_stats(period)
    return stats

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}
```

### 6. Entrypoint для API сервера

**Файл**: `src/api_server.py`

```python
"""Entrypoint для запуска Statistics API"""
import uvicorn
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### 7. Обновление зависимостей

**Файл**: `pyproject.toml`

Добавить в `dependencies`:

```toml
"fastapi>=0.104.0",
"uvicorn[standard]>=0.24.0",
```

### 8. Команды в Makefile

Добавить команды:

```makefile
# API server commands
api-run:
	uv run python -m src.api_server

api-dev:
	uv run uvicorn src.api.main:app --reload --port 8000

api-test:
	curl http://localhost:8000/api/stats?period=week | python -m json.tool
```

### 9. Создание **init**.py файлов

Создать пустые `__init__.py` для Python пакетов:

- `src/api/__init__.py`

### 10. Примеры запросов к API

**Файл**: `frontend/doc/api-examples.md`

Создать документ с примерами запросов для тестирования:

- curl команды для всех эндпоинтов
- Примеры с разными параметрами (day/week/month)
- Примеры использования с JavaScript fetch/axios
- Описание ожидаемых ответов

## Валидация

После реализации проверить:

1. ✅ API запускается на порту 8000
2. ✅ Swagger UI доступен по адресу http://localhost:8000/docs
3. ✅ GET /api/stats?period=day возвращает корректные данные
4. ✅ GET /api/stats?period=week возвращает другие данные
5. ✅ GET /api/stats?period=month возвращает данные за месяц
6. ✅ Данные соответствуют контракту из `api-contract-example.json`
7. ✅ Команда `make api-test` успешно выполняется

## Файлы для создания/изменения

**Новые файлы**:

- `frontend/doc/dashboard-requirements.md` - функциональные требования
- `frontend/doc/api-contract-example.json` - пример JSON контракта
- `src/api/__init__.py` - инициализация пакета
- `src/api/models.py` - dataclasses для API
- `src/api/stat_collector.py` - интерфейс StatCollector
- `src/api/mock_stat_collector.py` - Mock реализация
- `src/api/main.py` - FastAPI приложение
- `src/api_server.py` - entrypoint

**Изменяемые файлы**:

- `pyproject.toml` - добавить fastapi и uvicorn
- `Makefile` - добавить команды api-run, api-dev, api-test

### To-dos

- [ ] Создать документ функциональных требований к дашборду (frontend/doc/dashboard-requirements.md)
- [ ] Создать модели данных API контракта (src/api/models.py)
- [ ] Создать пример JSON контракта (frontend/doc/api-contract-example.json)
- [ ] Создать интерфейс StatCollector (src/api/stat_collector.py)
- [ ] Реализовать MockStatCollector с генерацией тестовых данных (src/api/mock_stat_collector.py)
- [ ] Создать FastAPI приложение с эндпоинтами (src/api/main.py)
- [ ] Создать entrypoint для запуска API (src/api_server.py)
- [ ] Добавить fastapi и uvicorn в pyproject.toml и выполнить uv sync
- [ ] Добавить команды api-run, api-dev, api-test в Makefile
- [ ] Протестировать API: запуск, Swagger UI, все эндпоинты с разными периодами