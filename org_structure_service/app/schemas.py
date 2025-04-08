from pydantic import BaseModel


class TeamStructureCreate(BaseModel):
    team_id: int
    structure_type: str


class DepartmentCreate(BaseModel):
    team_id: int
    name: str
    parent_department_id: int | None = None


class EmployeeStructureCreate(BaseModel):
    user_id: int
    department_id: int | None = None
    role: str
    manager_id: int | None = None


class EmployeeManagerCreate(BaseModel):
    employee_structure_id: int
    manager_id: int
    context: str


class Employee(BaseModel):
    """Модель сотрудника"""

    employee_id: int
    role: str
    managers: list[int | dict]  # Может быть просто ID или словарь {"manager_id": int, "context": str}

    model_config = {"from_attributes": True}


class SDepartment(BaseModel):
    """Модель отдела"""

    id: int
    name: str
    division_id: int | None = None
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

    structure_type: str
    hierarchy: dict[str, list[SDivision]] | dict[str, list[SDepartment]]  # "divisions" или "departments"

    model_config = {"from_attributes": True}
