# План: Спринт D2 - Развертывание на сервер

## Цель

Создать инструкцию и файлы для ручного развертывания приложения на production сервере с использованием готовых Docker образов из ghcr.io.

## Контекст

**Выполнено в D1:**
- Docker образы опубликованы в ghcr.io/nvalkg (bot, api, frontend)
- Образы доступны публично (docker login не требуется)
- `docker-compose.registry.yml` для использования готовых образов

**Параметры сервера:**
- IP: 83.147.246.172
- Пользователь: systech
- SSH ключ: `systech_admin_key.txt` (в корне проекта)
- Рабочая директория: `/opt/systech/nvalkg`
- Порты: API - 8005, Frontend - 3005
- Docker и Docker Compose установлены

**Развертываемые сервисы:**
- PostgreSQL (база данных)
- Bot (Telegram бот)
- API (FastAPI, порт 8005)
- Frontend (Next.js, порт 3005)

## Структура файлов

```
devops/
├── docker-compose.prod.yml      # новый - production конфигурация
├── .env.production.example      # новый - шаблон переменных окружения
└── doc/
    ├── guides/
    │   └── manual-deploy.md     # новый - пошаговая инструкция
    ├── plans/
    │   └── d2-manual-deploy.md  # новый - этот документ
    └── devops-roadmap.md        # обновить - статус D2
```

## Шаги реализации

### 1. Создать docker-compose.prod.yml

Файл: `devops/docker-compose.prod.yml`

**Основные изменения относительно docker-compose.registry.yml:**
- Использование образов из `ghcr.io/nvalkg` (публичные)
- Порты: API - 8005, Frontend - 3005
- PostgreSQL порт: 5432 (внутренний, без внешнего expose)
- Переменная NEXT_PUBLIC_API_URL для Frontend: `http://83.147.246.172:8005`
- env_file: `.env` (на сервере будет `.env.production`)
- Все сервисы с `restart: unless-stopped`
- Удалить `container_name` для гибкости
- Volume для PostgreSQL: `postgres_data_prod`

**Структура:**
```yaml
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment: ...
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
    healthcheck: ...

  bot:
    image: ghcr.io/nvalkg/aidd-bot:latest
    restart: unless-stopped
    depends_on: postgres (healthy)
    env_file: .env

  api:
    image: ghcr.io/nvalkg/aidd-api:latest
    restart: unless-stopped
    depends_on: postgres (healthy)
    ports: "8005:8000"
    env_file: .env

  frontend:
    image: ghcr.io/nvalkg/aidd-frontend:latest
    restart: unless-stopped
    depends_on: api
    ports: "3005:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://83.147.246.172:8005

volumes:
  postgres_data_prod:
```

### 2. Создать .env.production.example

Файл: `devops/.env.production.example`

**Содержание:**
```bash
# =============================================================================
# Production Environment Variables для AIDD Bot
# =============================================================================
# Скопируйте этот файл в .env.production и заполните значения
# На сервере переименуйте в .env перед запуском docker-compose

# -----------------------------------------------------------------------------
# Обязательные параметры (без них приложение не запустится)
# -----------------------------------------------------------------------------

# Токен Telegram бота (получить у @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# API ключ для OpenRouter (https://openrouter.ai/)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# -----------------------------------------------------------------------------
# База данных PostgreSQL
# -----------------------------------------------------------------------------

# URL подключения к БД (формат: postgresql+asyncpg://user:password@host:port/database)
# ⚠️ ВАЖНО: Используйте сильный пароль в production!
DATABASE_URL=postgresql+asyncpg://aidd:CHANGE_THIS_PASSWORD@postgres:5432/aidd

# Параметры БД (должны совпадать с docker-compose.prod.yml)
POSTGRES_USER=aidd
POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD
POSTGRES_DB=aidd

# -----------------------------------------------------------------------------
# Настройки LLM модели (необязательные, есть значения по умолчанию)
# -----------------------------------------------------------------------------

# Модель по умолчанию (примеры: openai/gpt-3.5-turbo, anthropic/claude-3-haiku)
DEFAULT_MODEL=openai/gpt-3.5-turbo

# Максимальное количество токенов в ответе (1-4096)
MAX_TOKENS=1000

# Temperature для генерации (0.0-2.0, меньше = более предсказуемо)
TEMPERATURE=0.7

# Количество сообщений в истории диалога (1-50)
MAX_HISTORY_MESSAGES=10

# -----------------------------------------------------------------------------
# Логирование
# -----------------------------------------------------------------------------

# Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# -----------------------------------------------------------------------------
# Системный промпт
# -----------------------------------------------------------------------------

# Путь к файлу с системным промптом (опционально)
# Если указан, будет загружен из файла, иначе используется SYSTEM_PROMPT
SYSTEM_PROMPT_FILE=/app/prompts/system_prompt.txt

# Текст системного промпта (используется если SYSTEM_PROMPT_FILE не указан)
SYSTEM_PROMPT=You are a helpful AI assistant.
```

**Комментарии на русском языке с описанием каждой переменной.**

### 3. Создать инструкцию manual-deploy.md

Файл: `devops/doc/guides/manual-deploy.md`

**Структура документа:**

#### Заголовок и описание
- Название: "Ручное развертывание на production сервере"
- Цель, требования, что будет развернуто

#### Раздел 1: Подготовка локально
- Проверка наличия файлов: `docker-compose.prod.yml`, `.env.production.example`, `systech_admin_key.txt`
- Копирование и заполнение `.env.production` на основе example
- Проверка прав SSH ключа (chmod 600 на Linux/Mac)

#### Раздел 2: Подключение к серверу
- Команда SSH с использованием ключа:
  ```bash
  ssh -i systech_admin_key.txt systech@83.147.246.172
  ```
- Проверка версий Docker и Docker Compose
- Создание рабочей директории `/opt/systech/nvalkg`

#### Раздел 3: Копирование файлов на сервер
- Копирование `docker-compose.prod.yml`:
  ```bash
  scp -i systech_admin_key.txt devops/docker-compose.prod.yml systech@83.147.246.172:/opt/systech/nvalkg/
  ```
- Копирование `.env.production` как `.env`:
  ```bash
  scp -i systech_admin_key.txt devops/.env.production systech@83.147.246.172:/opt/systech/nvalkg/.env
  ```
- Копирование файла промпта (если используется):
  ```bash
  scp -i systech_admin_key.txt prompts/system_prompt.txt systech@83.147.246.172:/opt/systech/nvalkg/
  ```

#### Раздел 4: Загрузка и запуск
- Переход в рабочую директорию
- Pull образов:
  ```bash
  docker-compose -f docker-compose.prod.yml pull
  ```
- Запуск в фоновом режиме:
  ```bash
  docker-compose -f docker-compose.prod.yml up -d
  ```

#### Раздел 5: Миграции базы данных
- Миграции выполняются автоматически при запуске бота (через entrypoint.sh)
- Проверка логов бота для подтверждения:
  ```bash
  docker-compose -f docker-compose.prod.yml logs bot
  ```

#### Раздел 6: Проверка работоспособности
- Проверка статуса контейнеров:
  ```bash
  docker-compose -f docker-compose.prod.yml ps
  ```
- Проверка логов каждого сервиса
- Проверка healthcheck PostgreSQL
- Проверка доступности API: `curl http://83.147.246.172:8005/health`
- Проверка Frontend в браузере: `http://83.147.246.172:3005`
- Тестирование бота в Telegram

#### Раздел 7: Управление сервисами
- Просмотр логов: `docker-compose logs -f [service]`
- Остановка: `docker-compose down`
- Перезапуск: `docker-compose restart [service]`
- Обновление образов: `docker-compose pull && docker-compose up -d`

#### Раздел 8: Troubleshooting
- Проблемы с подключением к БД
- Проблемы с портами
- Проблемы с миграциями
- Проблемы с сетевым доступом

#### Раздел 9: Backup и безопасность
- Рекомендации по backup PostgreSQL
- Настройка firewall (если нужно)
- Мониторинг логов

### 4. Создать план спринта d2-manual-deploy.md

Файл: `devops/doc/plans/d2-manual-deploy.md`

**Содержание:**
- Копия этого плана в структурированном виде
- Цель спринта
- Контекст (что было в D0, D1)
- Детальное описание каждого файла
- Чеклист для проверки
- Ссылки на созданные файлы

### 5. Обновить devops-roadmap.md

Файл: `devops/doc/devops-roadmap.md`

**Изменения:**
- Обновить статус D2 с "📋 Planned" на "✅ Completed"
- Добавить дату завершения
- Добавить ссылку на план: `[План спринта](plans/d2-manual-deploy.md)`
- Заполнить раздел "Спринт D2: Развертывание на сервер" с описанием реализованного
- Список созданных файлов и артефактов

## Ключевые особенности

**Безопасность:**
- Все секреты в `.env` файле
- SSH ключ с правильными правами (600)
- Сильный пароль БД в production

**Надежность:**
- Все сервисы с `restart: unless-stopped`
- Healthcheck для PostgreSQL
- Зависимости между сервисами (depends_on)

**Простота:**
- Все команды готовы к копированию
- Четкие пояснения на русском языке
- Секция troubleshooting для типичных проблем

**Готовность к автоматизации:**
- Все шаги можно автоматизировать в D3
- Четкая структура команд
- Переменные окружения вынесены в .env

## Проверка результата

После выполнения плана должны быть созданы:

1. ✅ `devops/docker-compose.prod.yml` - production конфигурация
2. ✅ `devops/.env.production.example` - шаблон переменных окружения
3. ✅ `devops/doc/guides/manual-deploy.md` - пошаговая инструкция
4. ✅ `devops/doc/plans/d2-manual-deploy.md` - план спринта
5. ✅ `devops/doc/devops-roadmap.md` - обновлен статус D2

**Критерии успеха:**
- Инструкция понятна и пошагова
- Все команды можно скопировать и выполнить
- .env файл содержит все необходимые переменные с описанием
- docker-compose.prod.yml корректно настроен для production
- Roadmap обновлен

## Примечания

- Выполнение деплоя по инструкции остается на усмотрение пользователя
- Инструкция готова к использованию сразу после создания файлов
- В D3 планируется автоматизация через GitHub Actions


