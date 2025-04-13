import enum

from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    team_id: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    team_id: int

    model_config = {"from_attributes": True}


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class TeamRoleResponse(BaseModel):
    role: EmployeeRole
