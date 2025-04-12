from uuid import UUID

from pydantic import BaseModel

from app.models.teams import EmployeeRole


class TeamCreate(BaseModel):
    name: str
    description: str


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str
    team_code: UUID

    model_config = {"from_attributes": True}


class AddEmployee(BaseModel):
    employee_id: int
    role: EmployeeRole = EmployeeRole.EMPLOYEE


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class TeamEmployeeResponse(BaseModel):
    id: int
    employee_id: int
    team_id: int
    role: EmployeeRole
