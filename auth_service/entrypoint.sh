#!/bin/bash
alembic upgrade head
python3 app/load_fixtures.py
uvicorn app.main:app --host 0.0.0.0 --port 8000