<!-- 0df882c5-ed2d-446c-a763-e87cfccafc29 56a83900-9e96-4ee5-bd8e-8eb2b91dadb8 -->
# План: Спринт D1 - Build & Publish

## Цель

Автоматическая сборка и публикация Docker образов в GitHub Container Registry (ghcr.io) с публичным доступом.

## Контекст

**Выполнено в D0:**

- 3 Dockerfile (bot, api, frontend) в `devops/`
- `devops/docker-compose.yml` для локальной сборки
- Образы собираются локально через `docker-compose up`

**Требуется в D1:**

- GitHub Actions для автоматической сборки
- Публикация в ghcr.io с именами: `aidd-bot`, `aidd-api`, `aidd-frontend`
- Поддержка локальной сборки и использования образов из registry
- Тестирование workflow на отдельной ветке

## Структура файлов

```
.github/workflows/
├── quality.yml              # существующий
└── build.yml                # новый - сборка образов

devops/
├── docker-compose.yml       # существующий - локальная сборка
├── docker-compose.registry.yml  # новый - образы из registry
└── doc/
    ├── guides/
    │   ├── docker-quickstart.md  # обновить
    │   └── github-actions-intro.md  # новый
    ├── plans/
    │   └── d1-build-publish.md   # этот документ
    └── devops-roadmap.md        # обновить
```

## Шаги реализации

### 1. Документация: Введение в GitHub Actions

Создать `devops/doc/guides/github-actions-intro.md`:

**Содержание:**

- Что такое GitHub Actions и workflows
- Принцип работы с Pull Requests (PR)
- Триггеры: `pull_request`, `push`, `workflow_dispatch`
- Matrix strategy для параллельной сборки
- GitHub Container Registry (ghcr.io)
- Public vs Private образы
- Автоматический `GITHUB_TOKEN` и permissions

**Структура:**

```markdown
# Введение в GitHub Actions

## Что такое GitHub Actions
- CI/CD платформа внутри GitHub
- Workflows в .github/workflows/*.yml
- Автоматический запуск при событиях

## Триггеры
- pull_request: при создании/обновлении PR
- push: при push в ветку
- workflow_dispatch: ручной запуск

## Matrix Strategy
Параллельная сборка нескольких образов...

## GitHub Container Registry
- Адрес: ghcr.io
- Публичные образы доступны без авторизации
- Настройка permissions в Actions
```

### 2. GitHub Actions Workflow

Создать `.github/workflows/build.yml`:

**Триггеры:**

- `pull_request` к main - только сборка (проверка что образы собираются)
- `push` в ветку `devops/d1-ci` - сборка + публикация (для тестирования)
- `push` в main - сборка + публикация

**Matrix strategy:**

```yaml
strategy:
  matrix:
    service:
   - name: bot
        dockerfile: devops/Dockerfile.bot
        image: aidd-bot
   - name: api
        dockerfile: devops/Dockerfile.api
        image: aidd-api
   - name: frontend
        dockerfile: devops/Dockerfile.frontend
        image: aidd-frontend
```

**Основная структура:**

```yaml
name: Build & Publish Docker Images

on:
  pull_request:
    branches: [main]
  push:
    branches: 
   - main
   - devops/d1-ci  # временно для тестирования

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [...]
    
    permissions:
      contents: read
      packages: write
    
    steps:
   - Checkout code
   - Set up Docker Buildx
   - Login to GHCR (только для push, не для PR)
   - Build and push
    - Теги: latest, commit SHA
    - Кэширование слоев
   - Output image tags
```

**Ключевые моменты:**

- Использовать `docker/build-push-action@v5`
- Кэширование через `cache-from/cache-to`
- Публикация только при push (не при PR)
- Теги: `latest` и `${{ github.sha }}`
- Образы: `ghcr.io/${{ github.repository_owner }}/aidd-bot:latest`

### 3. docker-compose.registry.yml

Создать `devops/docker-compose.registry.yml` - копия `docker-compose.yml` с использованием образов из registry:

**Изменения:**

```yaml
services:
  bot:
    image: ghcr.io/<username>/aidd-bot:latest  # вместо build
    container_name: aidd-bot
    # остальное без изменений

  api:
    image: ghcr.io/<username>/aidd-api:latest
    # ...

  frontend:
    image: ghcr.io/<username>/aidd-frontend:latest
    # ...
```

**Примечание:** В документации указать, что `<username>` нужно заменить на реальный GitHub username.

### 4. Сделать образы публичными

После первой публикации:

1. Перейти на https://github.com/<username>?tab=packages
2. Для каждого пакета (aidd-bot, aidd-api, aidd-frontend):

                        - Package settings → Danger Zone → Change visibility
                        - Выбрать "Public"
                        - Подтвердить

**Документировать в руководстве:** пошаговые скриншоты или детальное описание.

### 5. Обновить документацию

#### devops/doc/guides/docker-quickstart.md

Добавить секцию "Использование образов из Registry":

```markdown
## Использование образов из GitHub Container Registry

### Запуск с готовыми образами

# Скачать образы из registry
cd devops
docker-compose -f docker-compose.registry.yml pull

# Запустить сервисы
docker-compose -f docker-compose.registry.yml up

### Локальная сборка (для разработки)

# Сборка и запуск
docker-compose up --build
```

#### devops/README.md

Добавить информацию:

- Badge статуса сборки
- Ссылки на публичные образы
- Команды для работы с registry
```markdown
![Build Status](https://github.com/<username>/<repo>/actions/workflows/build.yml/badge.svg)

## Образы

Доступны публичные образы:
- ghcr.io/<username>/aidd-bot:latest
- ghcr.io/<username>/aidd-api:latest
- ghcr.io/<username>/aidd-frontend:latest
```


#### devops/doc/devops-roadmap.md

Обновить статус D1:

```markdown
| D1 | Build & Publish | ✅ Completed | [План спринта](plans/d1-build-publish.md) | <дата> |
```

### 6. Тестирование

**Локальное тестирование workflow (до merge):**

1. Создать ветку `devops/d1-ci`
2. Закоммитить все изменения
3. Push в ветку → проверить сборку и публикацию
4. Локально: pull образов и запуск через docker-compose.registry.yml
5. Проверить работу всех сервисов

**После merge в main:**

1. Проверить сборку на push в main
2. Убедиться что образы обновлены с тегом latest
3. Сделать образы публичными через UI
4. Протестировать скачивание без авторизации

**Smoke tests:**

```bash
# Pull без авторизации
docker pull ghcr.io/<username>/aidd-bot:latest
docker pull ghcr.io/<username>/aidd-api:latest
docker pull ghcr.io/<username>/aidd-frontend:latest

# Запуск через registry compose
cd devops
docker-compose -f docker-compose.registry.yml up

# Проверка:
# - Bot запустился
# - API доступен на :8000
# - Frontend доступен на :3000
# - Миграции выполнены
```

### 7. Создать план и отчеты

**Файлы документации:**

- `devops/doc/plans/d1-build-publish.md` - этот план
- `devops/doc/reports/d1-testing-report.md` - результаты тестирования
- `devops/doc/reports/d1-summary.md` - краткий итоговый отчет

## MVP требования

**Обязательно:**

- ✅ Workflow для сборки 3 образов (matrix strategy)
- ✅ Публикация в ghcr.io
- ✅ Образы публичные (без авторизации)
- ✅ Тегирование: latest и commit SHA
- ✅ docker-compose.registry.yml для использования образов
- ✅ Документация и инструкции
- ✅ Badge статуса сборки

**Пока не нужно:**

- ❌ Lint/test checks в build workflow (уже в quality.yml)
- ❌ Security scanning
- ❌ Multi-platform builds (amd64/arm64)
- ❌ Automated tests в CI
- ❌ Deployment triggers (будет в D3)

## Готовность к D2/D3

После D1 будет готово:

- **D2 (Ручной deploy):** Образы в registry, можно pull на сервер
- **D3 (Auto deploy):** Workflow сборки готов, добавим deploy step

## Примечания

- Временный триггер на `devops/d1-ci` удалить после успешного тестирования
- GitHub username захардкодить в docker-compose.registry.yml (или документировать замену)
- Образы будут доступны публично без `docker login`
- Кэширование слоев ускорит повторные сборки

### To-dos

- [ ] Создать devops/doc/guides/github-actions-intro.md с введением в GitHub Actions
- [ ] Создать .github/workflows/build.yml с matrix strategy для сборки 3 образов
- [ ] Создать devops/docker-compose.registry.yml для использования образов из ghcr.io
- [ ] Обновить devops/README.md, docker-quickstart.md и devops-roadmap.md
- [ ] Протестировать workflow на ветке devops/d1-ci и проверить публикацию образов
- [ ] Сделать образы публичными через GitHub UI и задокументировать процесс
- [ ] Выполнить smoke tests: pull образов без авторизации и запуск через docker-compose.registry.yml
- [ ] Создать отчеты: d1-testing-report.md и d1-summary.md