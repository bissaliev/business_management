from pydantic import BaseModel

from app.schemas.departments import SDepartment


class SDivision(BaseModel):
    """Модель дивизиона (для дивизионной структуры)"""

    id: int
    name: str
    departments: list["SDepartment"] = []

    model_config = {"from_attributes": True}


class DivisionResponse(BaseModel):
    """Модель дивизиона (для дивизионной структуры)"""

    id: int
    name: str

    model_config = {"from_attributes": True}
