import enum

from pydantic import BaseModel


class Status(str, enum.Enum):
    """Статус доступа пользователя"""

    USER = "пользователь"
    ADMIN = "админ"


class EmployeeRole(str, enum.Enum):
    """Роли работников команды"""

    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class User(BaseModel):
    """Модель ответа из User Service"""

    id: int
    email: str
    status: Status
    is_active: bool
    team_id: int
    role: EmployeeRole
