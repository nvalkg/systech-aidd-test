# Ручное развертывание на production сервере

Пошаговая инструкция по развертыванию приложения AIDD Bot на удаленном production сервере с использованием Docker образов из GitHub Container Registry.

## Цель

Развернуть все компоненты системы (PostgreSQL, Bot, API, Frontend) на production сервере с использованием готовых Docker образов.

## Требования

**Локально:**
- SSH клиент
- Доступ к SSH ключу `systech_admin_key.txt`
- Файлы для развертывания (создаются автоматически в процессе подготовки)

**На сервере (уже установлено):**
- Docker 20.10+
- Docker Compose 2.0+
- Доступ по SSH

**Параметры сервера:**
- IP адрес: `83.147.246.172`
- Пользователь: `systech`
- Рабочая директория: `/opt/systech/nvalkg`
- Порты: API - `8010`, Frontend - `3005`

## Что будет развернуто

| Сервис | Описание | Порт |
|--------|----------|------|
| PostgreSQL | База данных | Внутренний (5432) |
| Bot | Telegram бот | - |
| API | FastAPI backend | 8010 |
| Frontend | Next.js веб-интерфейс | 3005 |

---

## Шаг 1: Подготовка локально

### 1.1 Проверка наличия файлов

Убедитесь, что у вас есть необходимые файлы:

```bash
# В корне проекта
ls -la systech_admin_key.txt
ls -la devops/docker-compose.prod.yml
ls -la devops/env.production.example
```

**Ожидаемый результат:** Все файлы существуют.

### 1.2 Создание .env.production

Скопируйте шаблон и заполните реальными значениями:

```bash
# В директории devops
cd devops
cp env.production.example .env.production
```

Отредактируйте `.env.production` и укажите:

```bash
# Обязательно измените эти значения!
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # Ваш токен от @BotFather
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx                  # Ваш ключ OpenRouter
POSTGRES_PASSWORD=your_strong_password_here                # Сильный пароль для БД

# Обновите DATABASE_URL с новым паролем
DATABASE_URL=postgresql+asyncpg://aidd:your_strong_password_here@postgres:5432/aidd
```

⚠️ **ВАЖНО:**
- Используйте надежный пароль для `POSTGRES_PASSWORD`
- Не забудьте обновить пароль в `DATABASE_URL`
- Не коммитьте файл `.env.production` в git!

### 1.3 Проверка прав SSH ключа

**Для Linux/Mac:**
```bash
# Установите правильные права доступа
chmod 600 systech_admin_key.txt
```

**Для Windows:**
- Используйте PowerShell или Git Bash
- Права обычно настраиваются автоматически

---

## Шаг 2: Подключение к серверу

### 2.1 SSH подключение

Подключитесь к серверу с использованием SSH ключа:

```bash
# Из корневой директории проекта
ssh -i systech_admin_key.txt systech@83.147.246.172
```

**Ожидаемый результат:** Успешное подключение к серверу.

При первом подключении вас попросят подтвердить fingerprint сервера - введите `yes`.

### 2.2 Проверка окружения на сервере

После подключения проверьте версии установленного ПО:

```bash
# Проверка Docker
docker --version
# Ожидается: Docker version 20.10+ или выше

# Проверка Docker Compose
docker-compose --version
# Ожидается: Docker Compose version 2.0+ или выше
```

### 2.3 Создание рабочей директории

Создайте директорию для проекта:

```bash
# Создание директории (если не существует)
sudo mkdir -p /opt/systech/nvalkg

# Установка прав владения
sudo chown -R systech:systech /opt/systech/nvalkg

# Переход в рабочую директорию
cd /opt/systech/nvalkg
```

**Ожидаемый результат:** Директория создана, текущий путь `/opt/systech/nvalkg`.

### 2.4 Выход с сервера

Временно выйдите с сервера для копирования файлов:

```bash
exit
```

---

## Шаг 3: Копирование файлов на сервер

Выполните следующие команды **с локального компьютера** (не на сервере):

### 3.1 Копирование docker-compose.prod.yml

```bash
# Из корневой директории проекта
scp -i systech_admin_key.txt devops/docker-compose.prod.yml systech@83.147.246.172:/opt/systech/nvalkg/
```

**Ожидаемый результат:**
```
docker-compose.prod.yml    100%  1234    1.2KB/s   00:01
```

### 3.2 Копирование .env файла

```bash
# Из корневой директории проекта
scp -i systech_admin_key.txt devops/.env.production systech@83.147.246.172:/opt/systech/nvalkg/.env
```

⚠️ **Обратите внимание:** Файл копируется как `.env` (без `.production`).

**Ожидаемый результат:**
```
.env.production    100%  987    0.96KB/s   00:01
```

### 3.3 Копирование системного промпта (опционально)

Если вы используете кастомный системный промпт:

```bash
# Создайте директорию prompts на сервере
ssh -i systech_admin_key.txt systech@83.147.246.172 "mkdir -p /opt/systech/nvalkg/prompts"

# Скопируйте файл промпта
scp -i systech_admin_key.txt prompts/system_prompt.txt systech@83.147.246.172:/opt/systech/nvalkg/prompts/
```

**Примечание:** Если вы не используете файл промпта, этот шаг можно пропустить. Промпт будет использован из переменной `SYSTEM_PROMPT` в `.env`.

### 3.4 Копирование скрипта проверки (рекомендуется)

Скопируйте скрипт для автоматической проверки развертывания:

```bash
# Из корневой директории проекта
scp -i systech_admin_key.txt devops/scripts/deploy-check.sh systech@83.147.246.172:/opt/systech/nvalkg/
```

Этот скрипт пригодится для проверки работоспособности после развертывания (см. Шаг 6.7).

### 3.5 Проверка скопированных файлов

Подключитесь снова к серверу и проверьте файлы:

```bash
# Подключение
ssh -i systech_admin_key.txt systech@83.147.246.172

# Проверка файлов
cd /opt/systech/nvalkg
ls -la

# Ожидаемый вывод:
# docker-compose.prod.yml
# .env
# prompts/ (если копировали)
```

---

## Шаг 4: Загрузка образов и запуск

Все команды выполняются **на сервере** в директории `/opt/systech/nvalkg`.

### 4.1 Загрузка Docker образов

Загрузите готовые образы из GitHub Container Registry:

```bash
docker-compose -f docker-compose.prod.yml pull
```

**Ожидаемый результат:**
```
Pulling postgres  ... done
Pulling bot       ... done
Pulling api       ... done
Pulling frontend  ... done
```

**Время загрузки:** ~2-5 минут в зависимости от скорости интернета.

**Примечание:** Образы публичные, аутентификация не требуется.

### 4.2 Запуск сервисов

Запустите все сервисы в фоновом режиме:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Ожидаемый результат:**
```
Creating network "nvalkg_default" ...
Creating volume "nvalkg_postgres_data_prod" ...
Creating nvalkg_postgres_1 ... done
Creating nvalkg_bot_1      ... done
Creating nvalkg_api_1      ... done
Creating nvalkg_frontend_1 ... done
```

**Время запуска:** ~30-60 секунд.

---

## Шаг 5: Миграции базы данных

### 5.1 Автоматическое выполнение миграций

Миграции выполняются **автоматически** при запуске бота через `entrypoint.sh`.

Проверьте логи бота для подтверждения:

```bash
docker-compose -f docker-compose.prod.yml logs bot
```

**Ожидаемый вывод (примерно):**
```
bot_1  | Ожидание готовности PostgreSQL...
bot_1  | Запуск миграций...
bot_1  | INFO  [alembic.runtime.migration] Running upgrade -> 0f132edeb3b2, initial schema
bot_1  | INFO  [alembic.runtime.migration] Running upgrade 0f132edeb3b2 -> bd7b2d0ee30e, change user_id to bigint
bot_1  | Миграции выполнены! Запуск приложения...
bot_1  | INFO: Telegram bot started successfully
```

### 5.2 Ручной запуск миграций (если необходимо)

Если миграции не выполнились автоматически:

```bash
# Выполнить миграции вручную
docker-compose -f docker-compose.prod.yml exec bot alembic upgrade head
```

---

## Шаг 6: Проверка работоспособности

### 6.1 Статус контейнеров

Проверьте, что все контейнеры запущены:

```bash
docker-compose -f docker-compose.prod.yml ps
```

**Ожидаемый результат:** Все 4 сервиса в состоянии `Up`:
```
NAME                STATE      PORTS
postgres            Up (healthy)    5432/tcp
bot                 Up
api                 Up         0.0.0.0:8010->8000/tcp
frontend            Up         0.0.0.0:3005->3000/tcp
```

### 6.2 Проверка логов

Просмотрите логи каждого сервиса:

```bash
# Логи PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres

# Логи Bot
docker-compose -f docker-compose.prod.yml logs bot

# Логи API
docker-compose -f docker-compose.prod.yml logs api

# Логи Frontend
docker-compose -f docker-compose.prod.yml logs frontend

# Все логи вместе (с отслеживанием)
docker-compose -f docker-compose.prod.yml logs -f
```

**Что искать:**
- ✅ Нет сообщений об ошибках (ERROR)
- ✅ PostgreSQL показывает "database system is ready to accept connections"
- ✅ Bot показывает "Telegram bot started successfully"
- ✅ API показывает "Application startup complete"
- ✅ Frontend показывает "ready started server"

### 6.3 Healthcheck PostgreSQL

Проверьте статус healthcheck:

```bash
docker inspect nvalkg_postgres_1 | grep -A 5 "Health"
```

**Ожидаемый результат:** `"Status": "healthy"`

### 6.4 Проверка API

Проверьте доступность API через curl:

```bash
# На сервере
curl http://localhost:8010/health

# Или с вашего компьютера
curl http://83.147.246.172:8010/health
```

**Ожидаемый результат:**
```json
{"status":"ok"}
```

Проверьте документацию API:
```bash
curl http://83.147.246.172:8010/docs
# Должен вернуть HTML страницу Swagger
```

### 6.5 Проверка Frontend

Откройте в браузере:
```
http://83.147.246.172:3005
```

**Ожидаемый результат:**
- ✅ Страница загружается
- ✅ Отображается интерфейс приложения
- ✅ Нет ошибок в консоли браузера (F12)

### 6.6 Тестирование Telegram бота

1. Откройте Telegram
2. Найдите вашего бота (имя указано при создании в @BotFather)
3. Отправьте команду `/start`

**Ожидаемый результат:**
- ✅ Бот отвечает приветственным сообщением
- ✅ Можно вести диалог с ботом

### 6.7 Автоматическая проверка (рекомендуется)

Для быстрой и полной проверки развертывания используйте скрипт `deploy-check.sh`:

```bash
# 1. Скопируйте скрипт на сервер (если еще не скопирован)
# С локальной машины:
scp -i systech_admin_key.txt devops/scripts/deploy-check.sh systech@83.147.246.172:/opt/systech/nvalkg/

# 2. На сервере сделайте скрипт исполняемым
chmod +x deploy-check.sh

# 3. Запустите проверку
./deploy-check.sh
```

**Скрипт автоматически проверяет:**
- ✅ Системные требования (Docker, Docker Compose, curl)
- ✅ Наличие необходимых файлов
- ✅ Правильность настройки .env
- ✅ Статус всех контейнеров
- ✅ Healthcheck PostgreSQL
- ✅ Выполнение миграций
- ✅ Работоспособность всех сервисов
- ✅ Доступность портов
- ✅ Отсутствие ошибок в логах

**Пример вывода:**
```
========================================
Итоги проверки
========================================

Пройдено проверок: 28 / 28 (100%)

✓ Все проверки пройдены успешно!
  Развертывание работает корректно.
```

Подробнее см. [README скриптов](../../scripts/README.md).

---

## Шаг 7: Управление сервисами

### 7.1 Просмотр логов

```bash
# Все сервисы в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Конкретный сервис
docker-compose -f docker-compose.prod.yml logs -f api

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### 7.2 Перезапуск сервисов

```bash
# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.prod.yml restart api
docker-compose -f docker-compose.prod.yml restart bot
docker-compose -f docker-compose.prod.yml restart frontend
```

### 7.3 Остановка сервисов

```bash
# Остановка всех сервисов (контейнеры остаются)
docker-compose -f docker-compose.prod.yml stop

# Остановка и удаление контейнеров (данные БД сохраняются)
docker-compose -f docker-compose.prod.yml down

# Остановка и удаление контейнеров + volumes (⚠️ УДАЛИТ ДАННЫЕ БД!)
docker-compose -f docker-compose.prod.yml down -v
```

### 7.4 Обновление образов

Когда вышла новая версия приложения:

```bash
# 1. Загрузить новые образы
docker-compose -f docker-compose.prod.yml pull

# 2. Пересоздать и перезапустить контейнеры
docker-compose -f docker-compose.prod.yml up -d

# Docker Compose автоматически пересоздаст только изменившиеся контейнеры
```

### 7.5 Просмотр использования ресурсов

```bash
# Статистика в реальном времени
docker stats

# Занятое место
docker system df
```

---

## Шаг 8: Troubleshooting

### Проблема 1: Контейнер не запускается

**Симптомы:** `docker-compose ps` показывает статус `Restarting` или `Exited`.

**Решение:**
```bash
# Проверьте логи проблемного сервиса
docker-compose -f docker-compose.prod.yml logs <service_name>

# Проверьте переменные окружения
docker-compose -f docker-compose.prod.yml config
```

### Проблема 2: Ошибка подключения к БД

**Симптомы:** В логах bot или api видно "connection refused" или "could not connect to server".

**Решение:**
```bash
# 1. Проверьте статус PostgreSQL
docker-compose -f docker-compose.prod.yml ps postgres

# 2. Проверьте логи PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres

# 3. Проверьте healthcheck
docker inspect <postgres_container_id> | grep Health

# 4. Убедитесь, что DATABASE_URL в .env правильный
cat .env | grep DATABASE_URL
```

### Проблема 3: Порты заняты

**Симптомы:** "bind: address already in use".

**Решение:**
```bash
# Проверьте, какой процесс использует порт
sudo netstat -tulpn | grep 8010
sudo netstat -tulpn | grep 3005

# Остановите процесс или измените порты в docker-compose.prod.yml
```

### Проблема 4: Не выполнились миграции

**Симптомы:** Ошибки при обращении к БД, таблицы не существуют.

**Решение:**
```bash
# Выполните миграции вручную
docker-compose -f docker-compose.prod.yml exec bot alembic upgrade head

# Проверьте логи
docker-compose -f docker-compose.prod.yml logs bot
```

### Проблема 5: Frontend не может подключиться к API

**Симптомы:** Ошибки сети в браузере при обращении к API.

**Решение:**
```bash
# 1. Проверьте, что API доступен
curl http://83.147.246.172:8010/health

# 2. Проверьте переменную NEXT_PUBLIC_API_URL
docker-compose -f docker-compose.prod.yml config | grep NEXT_PUBLIC_API_URL

# 3. Если нужно, обновите URL в docker-compose.prod.yml и перезапустите
docker-compose -f docker-compose.prod.yml up -d frontend
```

### Проблема 6: Нет места на диске

**Симптомы:** "no space left on device".

**Решение:**
```bash
# Проверьте использование места
df -h

# Очистите неиспользуемые Docker ресурсы
docker system prune -a

# Удалите старые образы
docker image prune -a
```

---

## Шаг 9: Backup и безопасность

### 9.1 Backup базы данных

Регулярно создавайте резервные копии PostgreSQL:

```bash
# Создание backup
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U aidd aidd > backup_$(date +%Y%m%d_%H%M%S).sql

# Сохраните backup в безопасном месте
# Можно настроить cron для автоматического backup
```

### 9.2 Восстановление из backup

```bash
# Остановите сервисы (кроме postgres)
docker-compose -f docker-compose.prod.yml stop bot api frontend

# Восстановите данные
cat backup_20241018_120000.sql | docker-compose -f docker-compose.prod.yml exec -T postgres psql -U aidd aidd

# Запустите сервисы
docker-compose -f docker-compose.prod.yml start bot api frontend
```

### 9.3 Безопасность

**Рекомендации:**

1. **Firewall:** Настройте firewall, чтобы открыть только необходимые порты:
   ```bash
   sudo ufw allow 22/tcp   # SSH
   sudo ufw allow 8010/tcp # API
   sudo ufw allow 3005/tcp # Frontend
   sudo ufw enable
   ```

2. **Обновления:** Регулярно обновляйте образы и систему:
   ```bash
   # Обновление образов приложения
   docker-compose -f docker-compose.prod.yml pull
   docker-compose -f docker-compose.prod.yml up -d

   # Обновление системы
   sudo apt update && sudo apt upgrade -y
   ```

3. **Мониторинг логов:**
   ```bash
   # Настройте регулярную проверку логов
   docker-compose -f docker-compose.prod.yml logs --tail=100
   ```

4. **Защита .env файла:**
   ```bash
   chmod 600 .env
   # Никогда не коммитьте .env в git!
   ```

---

## Полезные команды

```bash
# Быстрая проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Перезапуск с обновлением
docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d

# Просмотр всех логов
docker-compose -f docker-compose.prod.yml logs -f --tail=50

# Очистка системы
docker system prune -a --volumes

# Вход в контейнер (для отладки)
docker-compose -f docker-compose.prod.yml exec api bash
docker-compose -f docker-compose.prod.yml exec bot bash
```

---

## Чек-лист финальной проверки

- [ ] Все 4 контейнера запущены (`docker-compose ps`)
- [ ] PostgreSQL в статусе "healthy"
- [ ] API отвечает на `curl http://83.147.246.172:8010/health`
- [ ] Frontend доступен в браузере `http://83.147.246.172:3005`
- [ ] Telegram бот отвечает на команду `/start`
- [ ] Миграции выполнены (проверка логов bot)
- [ ] Нет ошибок в логах сервисов
- [ ] Скрипт `deploy-check.sh` проходит все проверки
- [ ] Создан backup базы данных
- [ ] Настроен firewall (опционально)

---

## Следующие шаги

После успешного развертывания:

1. **Мониторинг:** Настройте систему мониторинга (Prometheus, Grafana)
2. **Автоматизация:** В Спринте D3 будет настроено автоматическое развертывание через GitHub Actions
3. **CI/CD:** Полная автоматизация от push в main до деплоя на production
4. **Масштабирование:** При необходимости можно добавить Load Balancer и дополнительные инстансы

---

## Ссылки

- [Docker Quickstart](docker-quickstart.md)
- [DevOps Roadmap](../devops-roadmap.md)
- [План спринта D2](../plans/d2-manual-deploy.md)
