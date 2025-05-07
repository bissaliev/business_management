from pydantic import BaseModel

from app.models import StructureType
from app.schemas.divisions import SDepartment, SDivision


class TeamStructureCreate(BaseModel):
    team_id: int
    structure_type: StructureType


class TeamStructureResponse(BaseModel):
    """Модель ответа эндпоинта"""

    team_id: int
    structure_type: StructureType
    divisions: list["SDivision"] = []
    departments: list["SDepartment"] = []

    model_config = {"from_attributes": True}


class TeamStructureResponseShort(BaseModel):
    """Модель ответа эндпоинта"""

    team_id: int
    structure_type: StructureType

    model_config = {"from_attributes": True}
