from datetime import datetime

from pydantic import BaseModel, Field


class NewEventHook(BaseModel):
    """Модель для управления событиями через сервисы"""

    source_id: int = Field(alias="id")
    title: str
    description: str
    employee_id: int = Field(alias="creator_id")
    start_time: datetime
    end_time: datetime
    event_type: str = "meeting"

    model_config = {"from_attributes": True}
