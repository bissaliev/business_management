from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.tasks import TaskStatus


class TaskCreate(BaseModel):
    """Создание задач"""

    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: int
    team_id: int


class TaskUpdate(BaseModel):
    """Обновление задач"""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskResponse(BaseModel):
    """Модель ответа задачи"""

    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    creator_id: int
    assignee_id: int
    team_id: int

    model_config = {"from_attributes": True}
