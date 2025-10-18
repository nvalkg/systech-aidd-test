# Quick Reference - DevOps Commands

Быстрая шпаргалка по основным командам для работы с Docker и CI/CD.

## 🚀 Быстрый старт

### Первый запуск (с готовыми образами)

```bash
# 1. Настройте .env в корне проекта
cp .env.example .env
# Отредактируйте TELEGRAM_BOT_TOKEN и OPENROUTER_API_KEY

# 2. Запустите с готовыми образами
cd devops
export GITHUB_USERNAME=nvalkg
docker-compose -f docker-compose.registry.yml up
```

### Первый запуск (локальная сборка)

```bash
# 1. Настройте .env
cp .env.example .env

# 2. Соберите и запустите
cd devops
docker-compose up --build
```

## 🐳 Docker Compose

### Локальная сборка

```bash
cd devops

# Сборка и запуск
docker-compose up

# В фоновом режиме
docker-compose up -d

# Пересборка образов
docker-compose up --build

# Только сборка (без запуска)
docker-compose build

# Пересборка конкретного сервиса
docker-compose build bot
```

### Образы из Registry

```bash
cd devops

# Скачать образы
docker-compose -f docker-compose.registry.yml pull

# Запустить
docker-compose -f docker-compose.registry.yml up

# В фоновом режиме
docker-compose -f docker-compose.registry.yml up -d

# Обновить образы и перезапустить
docker-compose -f docker-compose.registry.yml pull
docker-compose -f docker-compose.registry.yml up -d
```

### Управление

```bash
# Просмотр статуса
docker-compose ps

# Логи всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f frontend

# Остановка без удаления
docker-compose stop

# Остановка и удаление контейнеров
docker-compose down

# Полная очистка (включая volumes)
docker-compose down -v

# Перезапуск конкретного сервиса
docker-compose restart bot
```

## 🔍 Отладка

### Проверка работоспособности

```bash
# PostgreSQL
docker ps | grep aidd-postgres
docker exec aidd-postgres psql -U aidd -d aidd -c "SELECT 1"

# API health check
curl http://localhost:8000/api/health

# API docs
curl http://localhost:8000/docs

# Frontend
curl http://localhost:3000

# Логи миграций
docker logs aidd-bot | grep "Миграции"
```

### Вход в контейнер

```bash
# Bot
docker exec -it aidd-bot bash

# API
docker exec -it aidd-api bash

# Frontend
docker exec -it aidd-frontend sh

# PostgreSQL
docker exec -it aidd-postgres psql -U aidd -d aidd
```

### Проверка образов

```bash
# Список локальных образов
docker images | grep aidd

# Информация об образе
docker inspect ghcr.io/nvalkg/aidd-bot:latest

# История слоев образа
docker history ghcr.io/nvalkg/aidd-bot:latest
```

## 📦 Работа с GitHub Container Registry

### Скачивание образов

```bash
# Без авторизации (для публичных образов)
docker pull ghcr.io/nvalkg/aidd-bot:latest
docker pull ghcr.io/nvalkg/aidd-api:latest
docker pull ghcr.io/nvalkg/aidd-frontend:latest

# Конкретный тег (commit SHA)
docker pull ghcr.io/nvalkg/aidd-bot:main-abc1234
```

### Авторизация (для приватных образов)

```bash
# Создайте Personal Access Token на GitHub с правами packages:read

# Авторизация
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Проверка
docker pull ghcr.io/nvalkg/aidd-bot:latest

# Выход
docker logout ghcr.io
```

### Просмотр информации

```bash
# Список тегов (через GitHub API)
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/users/nvalkg/packages/container/aidd-bot/versions

# Размер образа
docker images ghcr.io/nvalkg/aidd-bot:latest
```

## 🔄 GitHub Actions

### Просмотр статуса

```bash
# Через GitHub CLI
gh run list --workflow=build.yml

# Просмотр конкретного запуска
gh run view <run-id>

# Логи workflow
gh run view <run-id> --log
```

### Ручной запуск (если настроен workflow_dispatch)

```bash
# Через GitHub CLI
gh workflow run build.yml

# Через web UI
# GitHub → Actions → Build & Publish → Run workflow
```

### Отладка workflow

```bash
# Клонируйте act для локального запуска Actions
# https://github.com/nektos/act

# Установка (Linux/Mac)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Запуск workflow локально
act push
```

## 🧹 Очистка

### Очистка Docker

```bash
# Удалить остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune

# Удалить неиспользуемые volumes
docker volume prune

# Полная очистка (осторожно!)
docker system prune -a --volumes
```

### Очистка конкретного проекта

```bash
cd devops

# Остановить и удалить контейнеры + volumes
docker-compose down -v

# Удалить образы проекта
docker rmi aidd-bot aidd-api aidd-frontend

# Или для registry образов
docker rmi ghcr.io/nvalkg/aidd-bot:latest
docker rmi ghcr.io/nvalkg/aidd-api:latest
docker rmi ghcr.io/nvalkg/aidd-frontend:latest
```

## 🔧 Полезные алиасы

Добавьте в `.bashrc` или `.zshrc`:

```bash
# Docker Compose сокращения
alias dc='docker-compose'
alias dcu='docker-compose up'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcp='docker-compose ps'

# Registry compose
alias dcr='docker-compose -f docker-compose.registry.yml'
alias dcru='docker-compose -f docker-compose.registry.yml up'
alias dcrp='docker-compose -f docker-compose.registry.yml pull'

# Docker
alias dps='docker ps'
alias di='docker images'
alias drm='docker rm'
alias drmi='docker rmi'

# GitHub CLI
alias ghw='gh workflow'
alias ghr='gh run'
```

## 📊 Мониторинг

### Ресурсы контейнеров

```bash
# Использование ресурсов в реальном времени
docker stats

# Конкретные контейнеры
docker stats aidd-bot aidd-api aidd-frontend

# Использование диска
docker system df

# Детальная информация
docker system df -v
```

### Логи

```bash
# Последние N строк
docker-compose logs --tail=100 bot

# Логи за последние 10 минут
docker-compose logs --since=10m

# Логи с временными метками
docker-compose logs -t -f
```

## 🆘 Troubleshooting

### Порты заняты

```bash
# Найти процесс, использующий порт
lsof -i :8000
netstat -tulpn | grep 8000

# Изменить порт в docker-compose.yml
ports:
  - "8001:8000"  # Изменить первое число
```

### Ошибки сборки

```bash
# Очистить build cache
docker builder prune

# Сборка без кэша
docker-compose build --no-cache

# Проверить .dockerignore
cat devops/.dockerignore.bot
```

### Проблемы с миграциями

```bash
# Проверить логи entrypoint
docker logs aidd-bot 2>&1 | grep -A 10 "miграции"

# Выполнить миграции вручную
docker exec aidd-bot .venv/bin/alembic upgrade head

# Откатить миграцию
docker exec aidd-bot .venv/bin/alembic downgrade -1
```

### Образ не скачивается

```bash
# Проверить доступность
curl -I https://ghcr.io/v2/nvalkg/aidd-bot/manifests/latest

# Проверить видимость пакета на GitHub
# https://github.com/nvalkg?tab=packages

# Очистить кэш Docker
docker system prune -a
```

## 📚 Дополнительная информация

- **Детальные руководства:** [devops/doc/guides/](doc/guides/)
- **DevOps Roadmap:** [devops/doc/devops-roadmap.md](doc/devops-roadmap.md)
- **Docker Quickstart:** [devops/doc/guides/docker-quickstart.md](doc/guides/docker-quickstart.md)
- **GitHub Actions Intro:** [devops/doc/guides/github-actions-intro.md](doc/guides/github-actions-intro.md)

---

**Обновлено:** 18.10.2025
**Версия:** 1.0
