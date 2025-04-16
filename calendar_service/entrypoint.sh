#!/bin/bash
alembic upgrade head
echo "Миграции выполнены в Calendar Service"
echo "Подключение сервера Calendar Service"
uvicorn app.main:app --host 0.0.0.0 --port 8000