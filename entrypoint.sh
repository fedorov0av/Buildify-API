#!/bin/bash

# Ждем, пока PostgreSQL станет доступен
dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout 60s

# Выполняем миграции с Alembic
poetry run alembic upgrade head
# poetry run alembic revision --autogenerate -m "Initial tables"
# Запускаем приложение (например, uvicorn)
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips=*
