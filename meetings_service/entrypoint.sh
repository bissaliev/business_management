#!/bin/bash
alembic upgrade head
echo "Миграции выполнены в Meeting Service"
echo "Подключение сервера Meeting Service"
uvicorn app.main:app --host 0.0.0.0 --port 8000