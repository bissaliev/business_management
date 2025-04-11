from pydantic import BaseModel


class EmployeeStructureCreate(BaseModel):
    employee_id: int
    department_id: int | None = None
    role: str
    manager_id: int | None = None


class EmployeeStructureUpdate(BaseModel):
    department_id: int | None = None
    role: str | None = None
    manager_id: int | None = None


class EmployeeManagerCreate(BaseModel):
    employee_structure_id: int
    manager_id: int
    context: str


class ExtraManager(BaseModel):
    manager_id: int
    context: str

    model_config = {"from_attributes": True}


class EmployeeResponse(BaseModel):
    """Модель сотрудника"""

    id: int
    employee_id: int
    department_id: int | None = None
    role: str
    manager_id: int | None = None

    model_config = {"from_attributes": True}
