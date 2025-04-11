from pydantic import UUID4, BaseModel

from app.models.teams import EmployeeRole


class TeamCreate(BaseModel):
    name: str
    description: str


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str
    team_code: UUID4

    model_config = {"from_attributes": True}


class AddEmployee(BaseModel):
    employee_id: int
    employee_role: EmployeeRole = EmployeeRole.EMPLOYEE
