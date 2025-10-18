# DevOps

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
├── docker-compose.yml          # Оркестрация всех сервисов
└── doc/
    ├── devops-roadmap.md       # Роадмап DevOps процессов
    ├── d0-completion-report.md # Отчет о спринте D0
    ├── plans/                  # Планы реализации спринтов
    └── guides/                 # Руководства и инструкции
```

## Основные команды

```bash
# Запуск
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

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

### Спринт D0 (✅ Completed)
- 📝 [План реализации](doc/plans/d0-basic-docker-setup.md) - детальный план
- 🎯 [Итоговый отчет](doc/reports/d0-summary.md) - результаты и выводы
- 🧪 [Отчет о тестировании](doc/reports/d0-testing-report.md) - smoke tests
- 📊 [Completion Report](doc/d0-completion-report.md) - краткая сводка
