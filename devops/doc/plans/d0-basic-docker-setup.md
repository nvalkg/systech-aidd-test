# План: Спринт D0 - Basic Docker Setup

## Цель

Запустить все сервисы локально через docker-compose одной командой.

## Контекст

- Bot: Telegram бот (Python + UV), запускается через `python -m src`
- API: FastAPI сервис (Python + UV), запускается через uvicorn
- Frontend: Next.js приложение (pnpm), стандартный `pnpm start`
- PostgreSQL: уже есть в docker-compose.yml
- Миграции: через alembic, запускаются автоматически при старте

## Структура файлов

Все Docker файлы будут в директории `devops/`:

```
devops/
├── Dockerfile.bot
├── Dockerfile.api
├── Dockerfile.frontend
├── docker-compose.yml
├── .dockerignore.bot
├── .dockerignore.api
├── .dockerignore.frontend
├── entrypoint.sh          # скрипт для миграций
└── doc/
    └── guides/
        └── docker-quickstart.md
```

## Шаги реализации

### 1. Создать Dockerfile.bot

```dockerfile
FROM python:3.11-slim
WORKDIR /app
# Установка UV
RUN pip install uv
# Копирование файлов зависимостей
COPY pyproject.toml uv.lock ./
# Установка зависимостей
RUN uv sync --frozen
# Копирование кода
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY alembic/ ./alembic/
COPY alembic.ini ./
# Копирование entrypoint
COPY devops/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "src"]
```

### 2. Создать Dockerfile.api

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY devops/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Создать Dockerfile.frontend

```dockerfile
FROM node:20-slim
WORKDIR /app
# Установка pnpm
RUN npm install -g pnpm
# Копирование файлов зависимостей
COPY frontend/app/package.json frontend/app/pnpm-lock.yaml ./
# Установка зависимостей
RUN pnpm install --frozen-lockfile
# Копирование кода
COPY frontend/app/ ./
# Сборка приложения
RUN pnpm build
# Запуск production сервера
CMD ["pnpm", "start"]
```

### 4. Создать .dockerignore файлы

**devops/.dockerignore.bot** и **devops/.dockerignore.api**:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage
*.log
.env
.venv/
venv/
node_modules/
frontend/
tests/
docs/
*.md
.git/
.gitignore
```

**devops/.dockerignore.frontend**:

```
node_modules/
.next/
out/
*.log
.env*.local
.git/
.gitignore
README.md
```

### 5. Создать entrypoint.sh

```bash
#!/bin/bash
set -e

echo "Ожидание готовности PostgreSQL..."
# Простая проверка доступности PostgreSQL
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "postgres" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "PostgreSQL еще не готов - ждем..."
  sleep 2
done

echo "PostgreSQL готов! Запуск миграций..."
uv run alembic upgrade head

echo "Миграции выполнены! Запуск приложения..."
exec "$@"
```

### 6. Создать devops/docker-compose.yml

Объединяет существующий postgres с новыми сервисами:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: aidd-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: aidd
      POSTGRES_PASSWORD: aidd_dev_password
      POSTGRES_DB: aidd
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aidd -d aidd"]
      interval: 10s
      timeout: 5s
      retries: 5

  bot:
    build:
      context: ..
      dockerfile: devops/Dockerfile.bot
    container_name: aidd-bot
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}
      DATABASE_URL: postgresql+asyncpg://aidd:aidd_dev_password@postgres:5432/aidd
      POSTGRES_USER: aidd
      POSTGRES_PASSWORD: aidd_dev_password
      POSTGRES_DB: aidd
    env_file:
      - ../.env

  api:
    build:
      context: ..
      dockerfile: devops/Dockerfile.api
    container_name: aidd-api
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://aidd:aidd_dev_password@postgres:5432/aidd
      OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}
      POSTGRES_USER: aidd
      POSTGRES_PASSWORD: aidd_dev_password
      POSTGRES_DB: aidd
    env_file:
      - ../.env

  frontend:
    build:
      context: ..
      dockerfile: devops/Dockerfile.frontend
    container_name: aidd-frontend
    restart: unless-stopped
    depends_on:
      - api
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000

volumes:
  postgres_data:
    driver: local
```

### 7. Создать .env.example

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenRouter API
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Configuration
DEFAULT_MODEL=openai/gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7
MAX_HISTORY_MESSAGES=10

# System Prompt
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt

# Database (для локальной разработки без Docker)
DATABASE_URL=postgresql+asyncpg://aidd:aidd_dev_password@localhost:5433/aidd

# Logging
LOG_LEVEL=INFO

# Statistics API (для тестирования)
USE_MOCK_STATS=false
```

### 8. Создать devops/doc/guides/docker-quickstart.md

Краткое руководство по запуску:

- Требования (Docker, Docker Compose)
- Настройка .env файла
- Запуск: `cd devops && docker-compose up`
- Проверка работоспособности
- Остановка: `docker-compose down`
- Полная очистка: `docker-compose down -v`

### 9. Обновить README.md

Добавить секцию "Запуск через Docker":

- Ссылка на devops/doc/guides/docker-quickstart.md
- Краткая инструкция запуска
- Преимущества Docker подхода

### 10. Протестировать

- Запуск: `cd devops && docker-compose up`
- Проверка логов всех сервисов
- Проверка работы бота в Telegram
- Проверка API: `curl http://localhost:8000/api/health`
- Проверка Frontend: открыть http://localhost:3000
- Проверка миграций: подключиться к БД и проверить таблицы

## Важные моменты MVP подхода

1. **Простые single-stage Dockerfile** - без multi-stage builds для ускорения разработки
2. **Автоматические миграции** - через entrypoint.sh при старте контейнера
3. **Базовый .dockerignore** - исключаем только критичные файлы
4. **Healthcheck для PostgreSQL** - гарантирует правильный порядок запуска
5. **Одна команда запуска** - `docker-compose up` для всего стека

## Файлы для создания/изменения

### Создать:

- `devops/Dockerfile.bot` - простой single-stage образ
- `devops/Dockerfile.api` - простой single-stage образ
- `devops/Dockerfile.frontend` - простой single-stage образ
- `devops/.dockerignore.bot` - базовое исключение файлов
- `devops/.dockerignore.api` - базовое исключение файлов
- `devops/.dockerignore.frontend` - базовое исключение файлов
- `devops/entrypoint.sh` - автоматический запуск миграций
- `devops/docker-compose.yml` - оркестрация 4 сервисов
- `.env.example` - шаблон переменных окружения
- `devops/doc/guides/docker-quickstart.md` - краткое руководство

### Изменить:

- `README.md` - добавить секцию "Запуск через Docker"
- `devops/doc/devops-roadmap.md` - обновить статус и добавить ссылку на план

## Чеклист выполнения

**Этап 1: Создание Dockerfiles (single-stage, MVP подход)**
- [ ] Создать простой Dockerfile.bot (Python + UV, single-stage)
- [ ] Создать простой Dockerfile.api (Python + UV, single-stage)
- [ ] Создать простой Dockerfile.frontend (Node + pnpm, single-stage)

**Этап 2: Создание .dockerignore файлов**
- [ ] Создать .dockerignore.bot (базовое исключение файлов)
- [ ] Создать .dockerignore.api (базовое исключение файлов)
- [ ] Создать .dockerignore.frontend (базовое исключение файлов)

**Этап 3: Создание инфраструктурных файлов**
- [ ] Создать entrypoint.sh для автоматического запуска миграций при старте
- [ ] Создать devops/docker-compose.yml с 4 сервисами (postgres, bot, api, frontend)
- [ ] Создать .env.example с описанием всех переменных окружения

**Этап 4: Документация**
- [ ] Создать devops/doc/guides/docker-quickstart.md с кратким руководством
- [ ] Обновить README.md - добавить секцию "Запуск через Docker"

**Этап 5: Тестирование**
- [ ] Локальное тестирование: запустить docker-compose up и проверить работу всех сервисов
- [ ] Проверить работу бота в Telegram
- [ ] Проверить работу API через curl/браузер
- [ ] Проверить работу Frontend в браузере
- [ ] Проверить автоматическое применение миграций

**Этап 6: Финализация**
- [ ] Актуализировать devops/doc/devops-roadmap.md - обновить статус спринта D0 на ✅ Completed
- [ ] Добавить ссылку на план реализации в таблицу спринтов в devops-roadmap.md

