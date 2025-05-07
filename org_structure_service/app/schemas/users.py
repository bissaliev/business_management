import enum

from pydantic import BaseModel


class Status(str, enum.Enum):
    USER = "пользователь"
    ADMIN = "админ"


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class User(BaseModel):
    id: int
    email: str
    status: Status
    is_active: bool
    team_id: int
    role: EmployeeRole
