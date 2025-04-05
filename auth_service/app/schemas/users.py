from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    team_code: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    team_id: int | None

    model_config = {"from_attributes": True}
