#!/bin/sh
set -e

host="$DB_HOST"
port="$DB_PORT"

echo "⏳ Ожидание базы данных на $host:$port..."

# Ждем пока порт БД не будет открыт
while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ База данных доступна!"

# Выполняем миграции
alembic upgrade head

# Запускаем приложение
exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000