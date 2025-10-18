# Инструкция по тестированию Docker Setup

Пошаговая инструкция для проверки работы Docker окружения.

## Предварительная проверка

### 1. Проверьте наличие Docker

```bash
docker --version
# Ожидаемый результат: Docker version 20.10+ или выше

docker-compose --version
# Ожидаемый результат: Docker Compose version 2.0+ или выше
```

### 2. Проверьте наличие .env файла

```bash
# В корне проекта
ls .env
```

Если файл отсутствует:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте свои токены
```

### 3. Проверьте структуру devops

```bash
cd devops
ls
```

Должны быть файлы:
- ✅ Dockerfile.bot
- ✅ Dockerfile.api
- ✅ Dockerfile.frontend
- ✅ docker-compose.yml
- ✅ entrypoint.sh
- ✅ .dockerignore.bot
- ✅ .dockerignore.api
- ✅ .dockerignore.frontend

## Тестирование

### Этап 1: Сборка образов

```bash
# В директории devops
docker-compose build
```

**Ожидаемый результат:**
- Успешная сборка 3 образов: bot, api, frontend
- Нет ошибок компиляции
- Время: ~3-5 минут при первой сборке

**Проверка:**
```bash
docker images | grep aidd
# Должны быть образы: devops-bot, devops-api, devops-frontend
```

### Этап 2: Запуск сервисов

```bash
# В директории devops
docker-compose up
```

**Ожидаемый результат:**
- PostgreSQL запускается первым
- Healthcheck для PostgreSQL проходит успешно
- Bot и API ждут готовности PostgreSQL
- Автоматически применяются миграции
- Все 4 сервиса запускаются без ошибок

**Проверьте логи:**
```
✅ "PostgreSQL готов! Запуск миграций..."
✅ "Миграции выполнены! Запуск приложения..."
✅ "Бот запущен!"
✅ "AIDD API успешно инициализирован"
```

### Этап 3: Проверка PostgreSQL

```bash
# В новом терминале
docker ps | grep aidd-postgres
```

**Ожидаемый результат:**
- Статус: Up
- Health: healthy
- Порт: 0.0.0.0:5433->5432/tcp

**Подключение к БД:**
```bash
docker exec -it aidd-postgres psql -U aidd -d aidd
\dt
# Должны быть таблицы: alembic_version, conversations, users
\q
```

### Этап 4: Проверка API

```bash
# Health check
curl http://localhost:8000/api/health

# Ожидаемый результат: {"status":"ok"}

# Проверка статистики
curl http://localhost:8000/api/stats?period=week

# Ожидаемый результат: JSON с метриками
```

**Swagger документация:**
- Откройте: http://localhost:8000/docs
- Должна загрузиться интерактивная документация API

### Этап 5: Проверка Frontend

```bash
# Откройте в браузере
http://localhost:3000
```

**Ожидаемый результат:**
- Загружается страница дашборда
- Отображаются метрики (или "Нет данных")
- Нет ошибок в консоли браузера (F12)
- API запросы успешны (Network tab)

### Этап 6: Проверка Bot

1. Откройте Telegram
2. Найдите вашего бота (по имени из @BotFather)
3. Отправьте `/start`

**Ожидаемый результат:**
- Бот отвечает приветственным сообщением
- Отправьте любое сообщение
- Бот отвечает (генерация через LLM)

**Проверка логов бота:**
```bash
docker-compose logs bot | tail -20
```

### Этап 7: Проверка миграций

```bash
# Проверка в логах bot
docker-compose logs bot | grep "Миграции выполнены"

# Проверка в логах api
docker-compose logs api | grep "Миграции выполнены"

# Проверка версии миграций в БД
docker exec -it aidd-postgres psql -U aidd -d aidd -c "SELECT version_num FROM alembic_version;"
```

**Ожидаемый результат:**
- Миграции выполнены для обоих сервисов
- В БД актуальная версия схемы

## Тестирование в фоновом режиме

```bash
# Остановите текущий docker-compose (Ctrl+C)

# Запустите в фоновом режиме
docker-compose up -d

# Проверьте статус
docker-compose ps

# Все сервисы должны быть Up
```

## Проверка логов

```bash
# Все логи
docker-compose logs -f

# Только bot
docker-compose logs -f bot

# Только api
docker-compose logs -f api

# Только frontend
docker-compose logs -f frontend

# Последние 50 строк
docker-compose logs --tail=50
```

## Перезапуск после изменений

```bash
# После изменения кода Python (bot/api)
docker-compose up --build bot api

# После изменения Frontend
docker-compose up --build frontend

# Полная пересборка
docker-compose build --no-cache
docker-compose up
```

## Очистка

### Мягкая очистка (сохраняет данные БД)

```bash
docker-compose down
```

### Полная очистка (удаляет ВСЕ данные)

```bash
docker-compose down -v
```

**⚠️ Внимание:** Команда `down -v` удалит:
- Все контейнеры
- Все данные PostgreSQL
- Volume с данными

## Проверочный чеклист

После выполнения всех тестов:

- [ ] PostgreSQL запускается и показывает healthy
- [ ] Миграции применяются автоматически
- [ ] Bot запускается и отвечает в Telegram
- [ ] API отвечает на /api/health
- [ ] Frontend загружается на localhost:3000
- [ ] Swagger docs доступен на localhost:8000/docs
- [ ] Логи не содержат критических ошибок
- [ ] Данные сохраняются между перезапусками (без -v)
- [ ] После docker-compose down -v все удаляется

## Troubleshooting

### Проблема: "Port already in use"

```bash
# Проверьте, какой процесс использует порт
netstat -ano | findstr :8000
# Остановите процесс или измените порт в docker-compose.yml
```

### Проблема: "Cannot connect to Docker daemon"

```bash
# Запустите Docker Desktop
# Или проверьте Docker service
```

### Проблема: "Build failed"

```bash
# Очистите Docker cache
docker system prune -a
docker-compose build --no-cache
```

### Проблема: "PostgreSQL не готов"

```bash
# Проверьте логи
docker-compose logs postgres

# Увеличьте timeout в docker-compose.yml
# healthcheck -> timeout: 10s
```

## Результат тестирования

✅ Все тесты пройдены - Docker setup готов к использованию!

Следующий этап: **Спринт D1 - Build & Publish** (автоматическая сборка через GitHub Actions)
