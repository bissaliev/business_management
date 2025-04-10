from pydantic import BaseModel

from app.schemas.employees import EmployeeResponse


class DepartmentCreate(BaseModel):
    team_id: int
    name: str
    parent_id: int | None = None
    division_id: int | None = None


class SDepartment(BaseModel):
    """Модель отдела"""

    id: int
    name: str
    division_id: int | None = None
    parent_id: int | None = None
    children: list["SDepartment"] = []
    employees: list[EmployeeResponse] = []

    model_config = {"from_attributes": True}


class DepartmentResponse(BaseModel):
    team_id: int
    name: str
    parent_id: int | None = None
