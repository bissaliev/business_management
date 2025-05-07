from pydantic import BaseModel

from app.models import EmployeeRole


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str


class TeamEmployeeResponse(BaseModel):
    """Модель ответа для работников из сервиса Team Service"""

    id: int
    employee_id: int
    team_id: int
    role: EmployeeRole
