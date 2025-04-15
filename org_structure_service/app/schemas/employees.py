from pydantic import BaseModel, EmailStr

from app.models import EmployeeRole


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    status: EmployeeRole


class TeamEmployeeResponse(BaseModel):
    """Модель ответа для работников из сервиса Team Service"""

    id: int
    employee_id: int
    team_id: int
    role: EmployeeRole


class EmployeeStructureCreate(BaseModel):
    employee_id: int
    department_id: int | None = None
    position: str
    manager_id: int | None = None


class EmployeeStructureUpdate(BaseModel):
    department_id: int | None = None
    position: str | None = None
    manager_id: int | None = None


class EmployeeManagerCreate(BaseModel):
    """Добавление дополнительного менеджера"""

    employee_structure_id: int
    manager_id: int
    context: str


class AddManager(BaseModel):
    """Добавление руководителя"""

    department_id: int
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
