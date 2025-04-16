from datetime import datetime

from pydantic import BaseModel

from app.models.events import EventType


class NewEventHook(BaseModel):
    """Создание событий через сервисы"""

    source_id: int
    title: str
    employee_id: int
    start_time: datetime
    end_time: datetime
    event_type: EventType


class EventParams(BaseModel):
    """Параметры для запросов на существование событий за определенный период"""

    employee_id: int
    start_time: datetime
    end_time: datetime


class EventDeleteParams(BaseModel):
    """Параметры для удаление событий через сервисы"""

    source_id: int
    employee_id: int
    event_type: EventType
