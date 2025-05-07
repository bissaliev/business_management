from pydantic import BaseModel


class EmployeeStructureCreate(BaseModel):
    employee_id: int
    position: str


class EmployeeStructureUpdate(BaseModel):
    position: str


class EmployeeManagerCreate(BaseModel):
    """Добавление дополнительного менеджера"""

    manager_id: int
    context: str


class AddManager(BaseModel):
    """Добавление руководителя"""

    manager_id: int


class EmployeeManagerResponse(BaseModel):
    id: int
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
    position: str
    manager_id: int | None = None

    model_config = {"from_attributes": True}
