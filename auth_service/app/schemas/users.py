import enum

from pydantic import UUID4, BaseModel, EmailStr

from app.models.users import Status


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class UserUpdate(BaseModel):
    """Обновление пользователя"""

    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserRestore(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    """Создание пользователя"""

    name: str
    email: EmailStr
    password: str
    team_code: UUID4


class UserResponse(BaseModel):
    """Модель ответа для пользователя"""

    id: int
    name: str
    email: EmailStr
    team_id: int

    model_config = {"from_attributes": True}


class UserTokenResponse(UserResponse):
    """Модель ответа для пользователя со статусом доступа"""

    role: "EmployeeRole" = EmployeeRole.EMPLOYEE
    status: Status


class Token(BaseModel):
    """Модель токена"""

    access_token: str
    token_type: str


class TeamRoleResponse(BaseModel):
    """Роль пользователя"""

    role: EmployeeRole
