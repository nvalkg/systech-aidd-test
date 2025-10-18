# Docker Quickstart

Краткое руководство по запуску проекта AIDD через Docker.

## Требования

- **Docker** (версия 20.10+)
- **Docker Compose** (версия 2.0+)

### Проверка установки

```bash
docker --version
docker-compose --version
```

## Быстрый старт

### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
# В корне проекта
cp .env.example .env
```

Отредактируйте `.env` и укажите свои токены:

```bash
# Обязательные параметры
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 2. Запуск всех сервисов

```bash
# Перейдите в директорию devops
cd devops

# Запустите все сервисы
docker-compose up
```

При первом запуске Docker:
- Скачает базовые образы (Python, Node, PostgreSQL)
- Соберет образы для bot, api и frontend
- Запустит все 4 сервиса
- Автоматически применит миграции базы данных

**Время первого запуска:** ~5-10 минут (зависит от скорости интернета)

### 3. Проверка работоспособности

После запуска проверьте каждый сервис:

#### PostgreSQL
```bash
# Должен показать "healthy"
docker ps | grep aidd-postgres
```

#### API
```bash
# Должен вернуть {"status": "ok"}
curl http://localhost:8000/api/health
```

#### Frontend
Откройте в браузере: http://localhost:3000

#### Bot
Найдите вашего бота в Telegram и отправьте `/start`

## Основные команды

### Запуск в фоновом режиме

```bash
docker-compose up -d
```

### Просмотр логов

```bash
# Логи всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f frontend
```

### Остановка сервисов

```bash
# Остановка без удаления контейнеров
docker-compose stop

# Остановка и удаление контейнеров
docker-compose down
```

### Полная очистка

```bash
# Удалить контейнеры и volumes (включая данные БД)
docker-compose down -v
```

**⚠️ Внимание:** Команда `down -v` удалит все данные из базы данных!

### Пересборка образов

```bash
# После изменения кода пересоберите образы
docker-compose build

# Или пересоберите и перезапустите
docker-compose up --build
```

## Доступные сервисы

| Сервис | Порт | URL | Описание |
|--------|------|-----|----------|
| Frontend | 3000 | http://localhost:3000 | Веб-интерфейс |
| API | 8000 | http://localhost:8000 | REST API |
| PostgreSQL | 5433 | localhost:5433 | База данных |
| Bot | - | Telegram | Telegram бот |

## Структура

```
devops/
├── Dockerfile.bot          # Образ для Telegram бота
├── Dockerfile.api          # Образ для API сервера
├── Dockerfile.frontend     # Образ для Frontend
├── docker-compose.yml      # Оркестрация сервисов
├── entrypoint.sh          # Скрипт инициализации (миграции)
└── .dockerignore.*        # Исключения для Docker build
```

## Troubleshooting

### Порты уже заняты

Если порты 3000, 8000 или 5433 уже используются, измените их в `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Изменить первое число
```

### Ошибка при сборке образов

```bash
# Очистите Docker cache
docker-compose build --no-cache
```

### Bot не запускается

Проверьте:
1. Правильность `TELEGRAM_BOT_TOKEN` в `.env`
2. Логи: `docker-compose logs bot`
3. Применились ли миграции

### API не отвечает

Проверьте:
1. Правильность `OPENROUTER_API_KEY` в `.env`
2. Логи: `docker-compose logs api`
3. Подключение к PostgreSQL: `docker-compose logs postgres`

### Frontend показывает ошибки

Проверьте:
1. API доступен: `curl http://localhost:8000/api/health`
2. Переменная `NEXT_PUBLIC_API_URL` в docker-compose.yml
3. Логи: `docker-compose logs frontend`

## Переход к production

Для production деплоя используйте:
- GitHub Container Registry (ghcr.io) для хранения образов
- Спринт D1: автоматическая сборка и публикация образов
- Спринт D2-D3: автоматическое развертывание на сервер

См. [DevOps Roadmap](../devops-roadmap.md) для деталей.

## Полезные ссылки

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [DevOps Roadmap](../devops-roadmap.md)
