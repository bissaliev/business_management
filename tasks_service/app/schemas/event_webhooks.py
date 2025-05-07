from datetime import datetime

from pydantic import BaseModel, Field


class NewEventHook(BaseModel):
    """Модель для управления событиями через сервисы"""

    source_id: int = Field(alias="id")
    title: str
    description: str
    employee_id: int = Field(alias="assignee_id")
    start_time: datetime
    end_time: datetime
    event_type: str = "task"

    model_config = {"from_attributes": True}
