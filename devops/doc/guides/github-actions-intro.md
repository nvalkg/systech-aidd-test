# Введение в GitHub Actions

Краткое руководство по GitHub Actions для автоматической сборки и публикации Docker образов.

## Что такое GitHub Actions

**GitHub Actions** - это встроенная CI/CD платформа GitHub, которая позволяет автоматизировать процессы разработки, тестирования и развертывания прямо в вашем репозитории.

### Основные концепции

- **Workflow (рабочий процесс)** - автоматизированный процесс, описанный в YAML файле
- **Job (задача)** - набор шагов, выполняемых на одном runner
- **Step (шаг)** - отдельная команда или action
- **Action** - переиспользуемый модуль для выполнения задач
- **Runner** - виртуальная машина, на которой выполняются workflows

### Где хранятся workflows

Все workflows хранятся в директории `.github/workflows/` в корне репозитория:

```
.github/
└── workflows/
    ├── quality.yml    # проверка качества кода
    ├── build.yml      # сборка и публикация образов
    └── deploy.yml     # развертывание (будет в D3)
```

## Триггеры (события)

Workflows запускаются автоматически при определенных событиях:

### pull_request

Запускается при создании или обновлении Pull Request:

```yaml
on:
  pull_request:
    branches: [main]  # только для PR в main ветку
```

**Использование:** Проверка, что изменения не ломают сборку.

### push

Запускается при push в указанные ветки:

```yaml
on:
  push:
    branches:
      - main
      - develop
```

**Использование:** Автоматическая сборка и публикация после мерджа.

### workflow_dispatch

Ручной запуск workflow через GitHub UI:

```yaml
on:
  workflow_dispatch:  # кнопка "Run workflow" в GitHub
```

**Использование:** Ручное развертывание, выполнение задач по требованию.

### Комбинация триггеров

Можно использовать несколько триггеров одновременно:

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:
```

## Принцип работы с Pull Requests

### Workflow для PR

```yaml
name: PR Checks

on:
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run checks
        run: make quality
```

### Жизненный цикл PR

1. **Создание PR** → Автоматически запускается workflow
2. **Push новых коммитов** → Workflow перезапускается
3. **Проверки passed** → Можно делать merge
4. **Merge в main** → Запускается workflow для main ветки

### Статусы проверок

- ✅ **Success** - все проверки прошли
- ❌ **Failed** - есть ошибки
- 🟡 **In Progress** - выполняется
- ⚪ **Pending** - в очереди

## Matrix Strategy

**Matrix strategy** позволяет запускать одну и ту же job с разными параметрами параллельно.

### Пример: сборка нескольких образов

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
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

    steps:
      - name: Build ${{ matrix.service.name }}
        run: |
          docker build -f ${{ matrix.service.dockerfile }} \
            -t ${{ matrix.service.image }} .
```

### Преимущества matrix

- ⚡ **Параллельное выполнение** - все варианты выполняются одновременно
- 📝 **Меньше дублирования кода** - одна job вместо трех
- 🔄 **Легко добавлять варианты** - просто добавить элемент в массив

### Как работает

1. GitHub Actions создает **отдельную job** для каждого элемента матрицы
2. Все jobs выполняются **параллельно** на разных runners
3. Доступ к параметрам через `${{ matrix.service.name }}`

## GitHub Container Registry (ghcr.io)

**GitHub Container Registry** - это встроенный Docker registry для хранения образов.

### Основная информация

- **Адрес:** `ghcr.io`
- **Формат образа:** `ghcr.io/<username>/<image>:<tag>`
- **Пример:** `ghcr.io/myuser/aidd-bot:latest`

### Публичные vs Приватные образы

#### Публичные образы (Public)

- ✅ Доступны всем без авторизации
- ✅ Можно скачать: `docker pull ghcr.io/user/image:tag`
- ✅ Не требуется `docker login`
- ✅ Идеально для open source проектов

#### Приватные образы (Private)

- 🔒 Требуется авторизация для скачивания
- 🔒 Нужен `docker login ghcr.io`
- 🔒 Доступны только авторизованным пользователям

### Как сделать образ публичным

После первой публикации образа:

1. Перейти на https://github.com/USERNAME?tab=packages
2. Выбрать пакет (например, `aidd-bot`)
3. **Package settings** → **Danger Zone** → **Change visibility**
4. Выбрать **Public**
5. Подтвердить изменение

### Авторизация в workflow

GitHub Actions автоматически предоставляет токен `GITHUB_TOKEN`:

```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Важно:** Для публикации нужны права `packages: write`.

## Permissions в GitHub Actions

Workflows должны явно указывать требуемые права доступа:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      contents: read      # чтение кода репозитория
      packages: write     # публикация образов в GHCR

    steps:
      # ...
```

### Основные права

- `contents: read` - чтение содержимого репозитория
- `contents: write` - запись в репозиторий (коммиты, теги)
- `packages: read` - чтение пакетов из registry
- `packages: write` - публикация пакетов в registry
- `pull-requests: write` - создание/изменение PR

## Автоматический GITHUB_TOKEN

GitHub автоматически создает токен для каждого workflow:

### Особенности

- ✅ Создается автоматически для каждого запуска
- ✅ Истекает после завершения workflow
- ✅ Доступен через `${{ secrets.GITHUB_TOKEN }}`
- ✅ Не требует ручной настройки

### Использование

```yaml
- name: Login to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### Ограничения

- ❌ Не может триггерить другие workflows (защита от циклов)
- ❌ Права ограничены настройками репозитория
- ✅ Для большинства задач достаточно

## Условное выполнение шагов

Можно выполнять шаги только при определенных условиях:

### Пример: публикация только при push

```yaml
- name: Login to GHCR
  if: github.event_name == 'push'  # только для push, не для PR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GITHUB_TOKEN }}

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    push: ${{ github.event_name == 'push' }}  # публикация только при push
    tags: |
      ghcr.io/${{ github.repository_owner }}/aidd-bot:latest
```

### Полезные условия

- `github.event_name == 'push'` - событие push
- `github.event_name == 'pull_request'` - событие PR
- `github.ref == 'refs/heads/main'` - ветка main
- `success()` - предыдущие шаги успешны
- `failure()` - хотя бы один шаг failed

## Кэширование Docker слоев

Кэширование ускоряет повторные сборки:

```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    file: devops/Dockerfile.bot
    push: ${{ github.event_name == 'push' }}
    tags: ghcr.io/${{ github.repository_owner }}/aidd-bot:latest
    cache-from: type=registry,ref=ghcr.io/${{ github.repository_owner }}/aidd-bot:buildcache
    cache-to: type=registry,ref=ghcr.io/${{ github.repository_owner }}/aidd-bot:buildcache,mode=max
```

### Преимущества

- ⚡ Быстрее сборка (используются кэшированные слои)
- 💰 Меньше расход ресурсов
- 🔄 Кэш хранится в registry

## Тегирование образов

### Рекомендуемые теги

```yaml
tags: |
  ghcr.io/${{ github.repository_owner }}/aidd-bot:latest
  ghcr.io/${{ github.repository_owner }}/aidd-bot:${{ github.sha }}
```

- `latest` - последняя версия
- `${{ github.sha }}` - конкретный коммит (полный SHA)
- `${{ github.ref_name }}` - имя ветки или тега
- `v1.0.0` - семантическое версионирование

### Примеры использования

```bash
# Всегда последняя версия
docker pull ghcr.io/user/aidd-bot:latest

# Конкретный коммит (воспроизводимость)
docker pull ghcr.io/user/aidd-bot:abc123def456...

# Версия релиза
docker pull ghcr.io/user/aidd-bot:v1.0.0
```

## Просмотр логов и отладка

### Где смотреть логи

1. Перейти в репозиторий на GitHub
2. Вкладка **Actions**
3. Выбрать workflow run
4. Кликнуть на job
5. Развернуть интересующий step

### Отладка

```yaml
- name: Debug info
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Branch: ${{ github.ref_name }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
```

### Useful context variables

- `github.event_name` - тип события (push, pull_request)
- `github.ref` - полная ссылка (refs/heads/main)
- `github.ref_name` - имя ветки (main)
- `github.sha` - SHA коммита
- `github.repository_owner` - владелец репозитория
- `github.actor` - кто запустил workflow

## Best Practices

### 1. Используйте конкретные версии actions

```yaml
# ✅ Хорошо - конкретная версия
- uses: actions/checkout@v4

# ❌ Плохо - latest может сломать workflow
- uses: actions/checkout@latest
```

### 2. Минимальные permissions

```yaml
# ✅ Хорошо - только необходимые права
permissions:
  contents: read
  packages: write

# ❌ Плохо - избыточные права
permissions: write-all
```

### 3. Кэшируйте зависимости

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 4. Используйте secrets для чувствительных данных

```yaml
# ✅ Хорошо
password: ${{ secrets.DATABASE_PASSWORD }}

# ❌ Плохо - хардкод секретов
password: "my-secret-password"
```

### 5. Тестируйте на ветках перед main

```yaml
on:
  push:
    branches:
      - main
      - 'feature/**'  # тестовые ветки
```

## Полезные ссылки

- [Документация GitHub Actions](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Marketplace Actions](https://github.com/marketplace?type=actions)

## Следующие шаги

После изучения этого руководства вы готовы:

1. ✅ Создавать workflows для CI/CD
2. ✅ Настраивать автоматическую сборку Docker образов
3. ✅ Публиковать образы в GitHub Container Registry
4. ✅ Использовать matrix strategy для параллельной сборки
5. ✅ Работать с триггерами и условиями

**Практика:** См. `.github/workflows/build.yml` в этом проекте - готовый пример workflow для сборки образов.
