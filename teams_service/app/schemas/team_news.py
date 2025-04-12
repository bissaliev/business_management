from datetime import datetime

from pydantic import BaseModel


class TeamNewsResponse(BaseModel):
    """Модель ответа для новостей команды"""

    id: int
    team_id: int
    title: str
    content: str
    created_at: datetime


class TeamNewsCreate(BaseModel):
    """Модель для создания новостей"""

    title: str
    content: str


class TeamNewsUpdate(BaseModel):
    """Модель для обновления новостей"""

    title: str | None = None
    content: str | None = None
