import enum
from datetime import datetime

from pydantic import BaseModel, Field


class EventType(str, enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class BaseMeetingEvent(BaseModel):
    event_type: str = "meeting"
    source_id: int = Field(alias="id")
    employee_id: int = Field(alias="creator_id")

    model_config = {"from_attributes": True}


class MeetingCreatedEvent(BaseMeetingEvent):
    title: str
    description: str
    start_time: datetime
    end_time: datetime


class MeetingUpdatedEvent(BaseMeetingEvent):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class MeetingDeletedEvent(BaseMeetingEvent):
    pass
