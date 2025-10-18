# DevOps Roadmap

Роадмап развития DevOps процессов для проекта AIDD Bot.

Подход: MVP - фокус на простоте и скорости, быстрый путь от локального запуска до автоматического развертывания на удаленном сервере.

## Таблица спринтов

| Код | Описание | Статус | План | Дата |
|-----|----------|--------|------|------|
| D0 | Basic Docker Setup | ✅ Completed | [План спринта](plans/d0-basic-docker-setup.md) | 18.10.2025 |
| D1 | Build & Publish | ✅ Completed | [План спринта](plans/d1-build-publish.md) | 18.10.2025 |
| D2 | Развертывание на сервер | ✅ Completed | [План спринта](plans/d2-manual-deploy.md) | 18.10.2025 |
| D3 | Auto Deploy | 📋 Planned | - | - |

**Легенда статусов:**
- 📋 Planned - запланировано
- 🚧 In Progress - в процессе
- ✅ Completed - завершено
- ⏸️ Paused - приостановлено

---

## Спринт D0: Basic Docker Setup ✅

**Статус:** ✅ Завершен 18.10.2025
**Цель:** Запустить все сервисы локально через docker-compose одной командой.

**Реализовано:**
- ✅ 3 Dockerfile (bot, api, frontend) - simple single-stage builds
- ✅ docker-compose.yml с 4 сервисами (PostgreSQL, Bot, API, Frontend)
- ✅ .dockerignore для каждого сервиса
- ✅ entrypoint.sh для автоматических миграций
- ✅ .env файл для переменных окружения
- ✅ Документация: Docker Quickstart, Testing Guide, Отчеты
- ✅ Тестирование: все сервисы работают, smoke tests пройдены

**Результат:**
Все сервисы запускаются одной командой `docker-compose up`. Локальная разработка готова.

**Ссылки:**
- [План реализации](plans/d0-basic-docker-setup.md)
- [Отчет о тестировании](reports/d0-testing-report.md)
- [Docker Quickstart](guides/docker-quickstart.md)

**Контекст:**
- Bot: Telegram бот, подключается к PostgreSQL
- API: FastAPI сервис для статистики
- Frontend: Next.js веб-интерфейс, подключается к API
- PostgreSQL: база данных (уже существует в проекте)

---

## Спринт D1: Build & Publish

**Статус:** ✅ Завершен
**Дата завершения:** 18.10.2025
**Цель:** Автоматическая сборка и публикация Docker образов в GitHub Container Registry.

**Реализовано:**
- ✅ GitHub Actions workflow (`.github/workflows/build.yml`)
- ✅ Matrix strategy для параллельной сборки 3 образов
- ✅ Автоматическая публикация в ghcr.io
- ✅ Тегирование: `latest` и commit SHA
- ✅ Кэширование Docker слоев для ускорения сборки
- ✅ `docker-compose.registry.yml` для использования образов из registry
- ✅ Документация: GitHub Actions intro, обновлен Docker Quickstart
- ✅ Badge статуса сборки в README

**Триггеры workflow:**
- Pull Request → сборка (проверка без публикации)
- Push в `main` → сборка + публикация
- Push в `devops/d1-ci` → временно для тестирования

**Образы:**
- `ghcr.io/nvalkg/aidd-bot:latest`
- `ghcr.io/nvalkg/aidd-api:latest`
- `ghcr.io/nvalkg/aidd-frontend:latest`

**Следующие шаги:**
- 🔄 Тестирование workflow на ветке `devops/d1-ci`
- 🔄 Сделать образы публичными через GitHub UI
- 🔄 Smoke tests: pull и запуск через docker-compose.registry.yml
- 🔄 Финальные отчеты после завершения тестирования

**Ссылки:**
- [План реализации](plans/d1-build-publish.md)
- [GitHub Actions Intro](guides/github-actions-intro.md)

---

## Спринт D2: Развертывание на сервер ✅

**Статус:** ✅ Завершен
**Дата завершения:** 18.10.2025
**Цель:** Развернуть приложение на удаленном сервере вручную (пошаговая инструкция).

**Реализовано:**
- ✅ `docker-compose.prod.yml` - production конфигурация с правильными портами (API: 8005, Frontend: 3005)
- ✅ `env.production.example` - шаблон переменных окружения с подробными комментариями на русском
- ✅ Детальная пошаговая инструкция по ручному развертыванию (9 разделов)
- ✅ SSH подключение к серверу с использованием ключа
- ✅ Копирование файлов на сервер через scp
- ✅ Загрузка образов из ghcr.io (публичные, без docker login)
- ✅ Автоматическое выполнение миграций при запуске
- ✅ Подробные разделы проверки работоспособности
- ✅ Скрипт `deploy-check.sh` для автоматической проверки развертывания
- ✅ Troubleshooting для типичных проблем
- ✅ Инструкции по backup и безопасности

**Параметры сервера:**
- IP: 83.147.246.172
- Пользователь: systech
- Рабочая директория: `/opt/systech/nvalkg`
- Порты: API - 8005, Frontend - 3005

**Результат:**
Готовая инструкция для развертывания на production сервере. Все команды готовы к копированию и выполнению. Инструкция включает все этапы от подготовки до проверки работоспособности.

**Ссылки:**
- [План реализации](plans/d2-manual-deploy.md)
- [Инструкция по ручному развертыванию](guides/manual-deploy.md)
- [docker-compose.prod.yml](../docker-compose.prod.yml)

**Созданные файлы:**
- `devops/docker-compose.prod.yml` - production конфигурация
- `devops/env.production.example` - шаблон переменных окружения
- `devops/doc/guides/manual-deploy.md` - пошаговая инструкция (9 разделов)
- `devops/doc/plans/d2-manual-deploy.md` - план спринта
- `devops/scripts/deploy-check.sh` - скрипт автоматической проверки развертывания
- `devops/scripts/README.md` - документация по скриптам

**Следующие шаги:**
В D3 будет реализована автоматизация развертывания через GitHub Actions.

---

## Спринт D3: Auto Deploy

**Цель:** Автоматическое развертывание на сервер через GitHub Actions по кнопке.

**Состав работ:**
- Создание GitHub Actions workflow для автоматического развертывания
- Настройка ручного триггера (workflow_dispatch) для запуска деплоя
- Реализация SSH подключения к серверу в рамках GitHub Actions
- Автоматическая загрузка новых версий образов (pull)
- Перезапуск сервисов через docker-compose
- Создание инструкции по настройке GitHub secrets (SSH_KEY, HOST, USER)
- Добавление уведомлений о статусе развертывания
- Обновление README.md с кнопкой "Deploy"

---

## Примечания

- Каждый спринт планируется в режиме Plan Mode перед началом реализации
- После завершения спринта в таблицу добавляется ссылка на план реализации
- Планы реализации хранятся в директории `devops/doc/plans/`
- Все инструкции и документация размещаются в директории `devops/doc/guides/`
