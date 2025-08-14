#!/bin/sh

echo "⏳ Esperando a que PostgreSQL esté listo..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL listo, ejecutando migraciones..."
alembic upgrade head

echo "🚀 Iniciando servidor..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir src
