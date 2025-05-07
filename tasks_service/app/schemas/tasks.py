from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.tasks import TaskStatus


class TaskCreate(BaseModel):
    """Создание задач"""

    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    assignee_id: int
    team_id: int


class TaskUpdate(BaseModel):
    """Обновление задач"""

    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None


class TaskResponse(BaseModel):
    """Модель ответа задачи"""

    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime
    creator_id: int
    assignee_id: int
    team_id: int

    model_config = {"from_attributes": True}
