from pydantic import BaseModel

from app.schemas.employees import EmployeeResponse


class DepartmentCreate(BaseModel):
    """Модель для создания департамента"""

    name: str
    parent_id: int | None = None
    division_id: int | None = None


class SDepartment(BaseModel):
    """Модель отдела(для орг. структуры)"""

    id: int
    name: str
    division_id: int | None = None
    parent_id: int | None = None
    children: list["SDepartment"] = []
    employees: list[EmployeeResponse] = []

    model_config = {"from_attributes": True}


class DepartmentResponse(BaseModel):
    """Модель ответа для департамента"""

    id: int
    team_id: int
    name: str
    parent_id: int | None = None
    division_id: int | None


class DepartmentUpdate(BaseModel):
    """Модель для обновления департамента"""

    team_id: int | None = None
    name: str | None = None
    parent_id: int | None = None
    division_id: int | None = None
