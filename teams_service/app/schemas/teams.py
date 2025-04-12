from uuid import UUID

from pydantic import BaseModel


class TeamCreate(BaseModel):
    """Создание команды"""

    name: str
    description: str


class TeamResponse(BaseModel):
    """Модель ответа команды"""

    id: int
    name: str
    description: str
    team_code: UUID

    model_config = {"from_attributes": True}


class TeamUpdate(BaseModel):
    """Модель обновления команды"""

    name: str | None = None
    description: str | None = None
