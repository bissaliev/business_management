#!/bin/bash
alembic upgrade head
echo "Миграции выполнены в Task Service"
echo "Подключение сервера Task Service"
uvicorn app.main:app --host 0.0.0.0 --port 8000