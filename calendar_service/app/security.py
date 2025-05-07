from fastapi import Header, HTTPException

from app.config import settings


def verify_api_key(x_api_key: str = Header(...)):
    """Функция верифицирует заголовок API KEY"""
    if x_api_key not in [settings.MEETING_API_KEY, settings.TASK_API_KEY]:
        raise HTTPException(status_code=403, detail="Invalid API Key")
