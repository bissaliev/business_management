from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.events import EventType


class EventCreate(BaseModel):
    """Создание события"""

    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime | None = None
    event_type: EventType = EventType.PERSONAL


class EventUpdate(BaseModel):
    """Обновление события"""

    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_type: EventType = EventType.PERSONAL


class EventOut(BaseModel):
    """Модель ответа события"""

    id: int
    employee_id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    event_type: EventType
    source_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
