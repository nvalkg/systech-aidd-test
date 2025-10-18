# DevOps

![Build Status](https://github.com/nvalkg/systech-aidd-test/actions/workflows/build.yml/badge.svg)

Директория для DevOps процессов и инфраструктуры проекта AIDD Bot.

## 🚀 Быстрый старт

Запуск всех сервисов одной командой:

```bash
# Убедитесь, что .env файл настроен в корне проекта
cd devops
docker-compose up
```

**Сервисы:**
- 🗄️ PostgreSQL: порт 5433
- 🤖 Bot: Telegram
- 🔌 API: http://localhost:8000
- 🌐 Frontend: http://localhost:3000

📖 **Подробное руководство:** [Docker Quickstart](doc/guides/docker-quickstart.md)

### Использование готовых образов

Образы автоматически собираются через GitHub Actions и публикуются в GitHub Container Registry:

```bash
# Запуск с готовыми образами (быстрее)
docker-compose -f docker-compose.registry.yml up
```

**Доступные публичные образы:**
- `ghcr.io/nvalkg/aidd-bot:latest`
- `ghcr.io/nvalkg/aidd-api:latest`
- `ghcr.io/nvalkg/aidd-frontend:latest`

Образы доступны без авторизации (`docker login` не требуется).

## Структура

```
devops/
├── Dockerfile.bot              # Образ для Telegram бота
├── Dockerfile.api              # Образ для API сервера
├── Dockerfile.frontend         # Образ для Frontend
├── .dockerignore.bot           # Исключения для bot
├── .dockerignore.api           # Исключения для api
├── .dockerignore.frontend      # Исключения для frontend
├── entrypoint.sh               # Скрипт для миграций
├── docker-compose.yml          # Локальная сборка образов
├── docker-compose.registry.yml # Использование образов из GHCR
└── doc/
    ├── devops-roadmap.md       # Роадмап DevOps процессов
    ├── d0-completion-report.md # Отчет о спринте D0
    ├── plans/                  # Планы реализации спринтов
    └── guides/                 # Руководства и инструкции
```

## Основные команды

### Локальная сборка

```bash
# Запуск с локальной сборкой
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

# Пересборка образов
docker-compose up --build
```

### Использование образов из registry

```bash
# Скачать образы из GHCR
docker-compose -f docker-compose.registry.yml pull

# Запуск с образами из registry
docker-compose -f docker-compose.registry.yml up

# В фоновом режиме
docker-compose -f docker-compose.registry.yml up -d
```

### Общие команды

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Полная очистка (включая данные БД)
docker-compose down -v
```

## Подход

MVP DevOps - фокус на простоте и скорости, быстрый путь от локального запуска до автоматического развертывания на удаленном сервере.

**Текущий статус:** ✅ Спринт D0 завершен - локальный запуск через Docker готов

## Документация

### Общее
- 📋 [DevOps Roadmap](doc/devops-roadmap.md) - план развития инфраструктуры
- 🐳 [Docker Quickstart](doc/guides/docker-quickstart.md) - руководство по запуску
- ⚡ [Quick Reference](QUICK-REFERENCE.md) - шпаргалка по командам
- 🎯 [Next Steps](NEXT-STEPS.md) - следующие шаги для завершения D1

### Руководства
- 🚀 [GitHub Actions Intro](doc/guides/github-actions-intro.md) - введение в CI/CD
- 🔓 [Make Images Public](doc/guides/make-images-public.md) - как сделать образы публичными
- 📚 [Все руководства](doc/README.md) - полный список документации

### Спринт D0 (✅ Completed)
- 📝 [План реализации](doc/plans/d0-basic-docker-setup.md) - детальный план
- 🎯 [Итоговый отчет](doc/reports/d0-summary.md) - результаты и выводы
- 🧪 [Отчет о тестировании](doc/reports/d0-testing-report.md) - smoke tests
- 📊 [Completion Report](doc/d0-completion-report.md) - краткая сводка

### Спринт D1 (🚧 In Progress)
- 📝 [План реализации](doc/plans/d1-build-publish.md) - детальный план
- 🎯 [Итоговый отчет](doc/reports/d1-summary.md) - результаты и выводы (в процессе)
- 🧪 [Отчет о тестировании](doc/reports/d1-testing-report.md) - чеклист тестирования
