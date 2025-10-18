# Пересборка Frontend с правильным API URL

## Проблема

Next.js встраивает переменные окружения `NEXT_PUBLIC_*` в JavaScript код **на этапе сборки**, а не берет их из окружения в runtime. 

Это означает, что если образ был собран с одним `NEXT_PUBLIC_API_URL`, то изменение переменной окружения в `docker-compose.yml` **не повлияет** на работу приложения.

## Решение

Для изменения API URL необходимо **пересобрать Frontend образ** с правильным значением переменной.

### Шаг 1: Пересборка образа локально

```bash
# Из корня проекта
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://83.147.246.172:8010 \
  -f devops/Dockerfile.frontend \
  -t ghcr.io/nvalkg/aidd-frontend:latest \
  .
```

### Шаг 2: Передача образа на сервер

**Вариант A: Через docker save/load (без registry)**

```bash
# Локально: сохранить образ в файл
docker save ghcr.io/nvalkg/aidd-frontend:latest -o frontend-image.tar

# Скопировать на сервер
scp -i systech_admin_key.txt frontend-image.tar systech@83.147.246.172:/opt/systech/nvalkg/

# На сервере: загрузить образ
ssh -i systech_admin_key.txt root@83.147.246.172
cd /opt/systech/nvalkg
docker load -i frontend-image.tar
docker compose -f docker-compose.prod.yml up -d frontend
rm frontend-image.tar
```

**Вариант B: Через GitHub Container Registry (требует аутентификации)**

```bash
# Локально: залогиниться и запушить
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker push ghcr.io/nvalkg/aidd-frontend:latest

# На сервере: обновить образ
ssh -i systech_admin_key.txt systech@83.147.246.172
cd /opt/systech/nvalkg
docker compose -f docker-compose.prod.yml pull frontend
docker compose -f docker-compose.prod.yml up -d frontend
```

### Шаг 3: Проверка

После перезапуска Frontend:

1. Откройте DevTools (F12) в браузере
2. Перейдите на вкладку Network
3. Обновите страницу Dashboard (Ctrl+Shift+R)
4. Найдите запрос к `stats?period=week`
5. Проверьте **Request URL** - должен быть `http://83.147.246.172:8010/api/stats?period=week`

## Важные замечания

### ⚠️ Dockerfile должен содержать ARG

Убедитесь, что в `devops/Dockerfile.frontend` есть:

```dockerfile
# Аргумент для API URL (передается через --build-arg)
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Сборка приложения
RUN pnpm build
```

### ⚠️ Порядок важен

ARG и ENV должны быть объявлены **ДО** команды `RUN pnpm build`, так как Next.js использует эти переменные на этапе сборки.

### ⚠️ Кэш Docker

Если используете кэш Docker, добавьте флаг `--no-cache` при сборке:

```bash
docker build --no-cache \
  --build-arg NEXT_PUBLIC_API_URL=http://83.147.246.172:8010 \
  -f devops/Dockerfile.frontend \
  -t ghcr.io/nvalkg/aidd-frontend:latest \
  .
```

## Для других окружений

### Development

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
  -f devops/Dockerfile.frontend \
  -t aidd-frontend:dev \
  .
```

### Staging

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://staging.example.com:8010 \
  -f devops/Dockerfile.frontend \
  -t ghcr.io/nvalkg/aidd-frontend:staging \
  .
```

### Production

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://83.147.246.172:8010 \
  -f devops/Dockerfile.frontend \
  -t ghcr.io/nvalkg/aidd-frontend:latest \
  .
```

## Автоматизация через GitHub Actions

В будущем (Sprint D3) будет настроен CI/CD pipeline, который автоматически:

1. Соберет образ с правильным API URL из переменной окружения
2. Запушит в GitHub Container Registry
3. Обновит образ на production сервере

См. `.github/workflows/build.yml` для деталей.

## Полезные ссылки

- [Next.js Environment Variables](https://nextjs.org/docs/pages/building-your-application/configuring/environment-variables)
- [Docker Build Args](https://docs.docker.com/engine/reference/commandline/build/#build-arg)
- [Manual Deploy Guide](manual-deploy.md)

