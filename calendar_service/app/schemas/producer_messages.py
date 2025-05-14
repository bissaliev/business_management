import enum
from datetime import datetime

from pydantic import BaseModel

from app.models.events import EventType


class MessageType(str, enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class BaseProducerMessage(BaseModel):
    source_id: int
    employee_id: int
    event_type: EventType = EventType.PERSONAL


class ProducerMessageCreate(BaseProducerMessage):
    """Создание события"""

    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime | None = None


class ProducerMessageUpdate(ProducerMessageCreate):
    pass


class ProducerMessageDelete(BaseProducerMessage):
    pass
