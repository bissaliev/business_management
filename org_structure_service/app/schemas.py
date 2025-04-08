from pydantic import BaseModel


class TeamStructureCreate(BaseModel):
    team_id: int
    structure_type: str


class DepartmentCreate(BaseModel):
    team_id: int
    name: str
    parent_department_id: int | None = None


class EmployeeStructureCreate(BaseModel):
    user_id: int
    department_id: int | None = None
    role: str
    manager_id: int | None = None


class EmployeeManagerCreate(BaseModel):
    employee_structure_id: int
    manager_id: int
    context: str
