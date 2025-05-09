import enum
from datetime import datetime

from pydantic import BaseModel, Field


class EventType(str, enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class BaseTaskEvent(BaseModel):
    event_type: str = "task"
    source_id: int = Field(alias="id")
    employee_id: int = Field(alias="assignee_id")

    model_config = {"from_attributes": True}


class TaskCreatedEvent(BaseTaskEvent):
    title: str
    description: str
    start_time: datetime
    end_time: datetime


class TaskUpdatedEvent(BaseTaskEvent):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class TaskDeletedEvent(BaseTaskEvent):
    pass
