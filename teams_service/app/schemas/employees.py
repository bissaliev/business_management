from pydantic import BaseModel, EmailStr

from app.models.teams import EmployeeRole


class UserResponse(BaseModel):
    """Модель ответа из user service"""

    id: int
    name: str
    email: EmailStr


class EmployeeUpdateRole(BaseModel):
    """Модель для обновления роли работника"""

    role: EmployeeRole


class AddEmployee(BaseModel):
    employee_id: int
    role: EmployeeRole = EmployeeRole.EMPLOYEE


class TeamEmployeeResponse(BaseModel):
    """Модель ответа для работников"""

    id: int
    employee_id: int
    team_id: int
    role: EmployeeRole


class EmployeeCreate(BaseModel):
    """Создание работника"""

    name: str
    email: EmailStr
    password: str
    team_code: str | None = None
