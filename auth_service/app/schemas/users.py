import enum

from pydantic import UUID4, BaseModel, EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserRestore(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    team_code: UUID4


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
