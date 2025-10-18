#!/bin/bash
set -e

echo "Ожидание готовности PostgreSQL..."
# Простая задержка для healthcheck
sleep 10

echo "Запуск миграций..."
.venv/bin/alembic upgrade head

echo "Миграции выполнены! Запуск приложения..."
# Активируем venv для запуска приложения
export PATH="/app/.venv/bin:$PATH"
exec "$@"
