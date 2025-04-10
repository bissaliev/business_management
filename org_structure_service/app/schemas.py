from pydantic import BaseModel

from app.models import StructureType


class TeamStructureCreate(BaseModel):
    team_id: int
    structure_type: StructureType


class DepartmentCreate(BaseModel):
    team_id: int
    name: str
    parent_id: int | None = None
    division_id: int | None = None


class EmployeeStructureCreate(BaseModel):
    user_id: int
    department_id: int | None = None
    role: str
    manager_id: int | None = None


class EmployeeManagerCreate(BaseModel):
    employee_structure_id: int
    manager_id: int
    context: str


class ExtraManager(BaseModel):
    manager_id: int
    context: str

    model_config = {"from_attributes": True}


class Employee(BaseModel):
    """Модель сотрудника"""

    employee_id: int
    role: str
    manager_id: int | None = None
    extra_managers: list[ExtraManager] = []

    model_config = {"from_attributes": True}


class SDepartment(BaseModel):
    """Модель отдела"""

    id: int
    name: str
    division_id: int | None = None
    parent_id: int | None = None
    children: list["SDepartment"] = []
    employees: list[Employee] = []

    model_config = {"from_attributes": True}


class SDivision(BaseModel):
    """Модель дивизиона (для дивизионной структуры)"""

    id: int
    name: str
    departments: list[SDepartment] = []

    model_config = {"from_attributes": True}


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


class DivisionResponse(BaseModel):
    """Модель дивизиона (для дивизионной структуры)"""

    id: int
    name: str

    model_config = {"from_attributes": True}


class DepartmentResponse(BaseModel):
    team_id: int
    name: str
    parent_department_id: int | None = None
