import enum

from pydantic import UUID4, BaseModel


class Status(str, enum.Enum):
    USER = "пользователь"
    ADMIN = "админ"


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class User(BaseModel):
    """Модель пользователя"""

    id: int
    email: str
    status: Status
    is_active: bool
    team_id: int
    role: EmployeeRole


class EmployeeCreate(BaseModel):
    """Тело запроса при получении по вебхуку"""

    team_code: UUID4
    employee_id: int


class EmployeeResponse(BaseModel):
    """Модель ответа при запросе по вебхуку"""

    employee_id: int
    team_id: int
