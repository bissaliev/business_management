from pydantic import BaseModel

from app.schemas.departments import SDepartment


class SDivision(BaseModel):
    """Модель дивизиона (для дивизионной структуры)"""

    id: int
    name: str
    departments: list["SDepartment"] = []

    model_config = {"from_attributes": True}


class DivisionCreate(BaseModel):
    """Модель для создания дивизии"""

    team_id: int
    name: str


class DivisionResponse(BaseModel):
    """Модель-ответ дивизии"""

    id: int
    team_id: int
    name: str

    model_config = {"from_attributes": True}


class DivisionUpdate(BaseModel):
    """Модель для обновления дивизии"""

    team_id: int | None = None
    name: str | None = None

    model_config = {"from_attributes": True}
