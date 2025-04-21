from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teams import TeamEmployee
from app.repositories.team_employee_repo import TeamEmployeeRepository
from app.repositories.team_repo import TeamRepository
from app.schemas.users import EmployeeCreate


class WebHookService:
    """Сервис для добавление сотрудника при регистрации на основе кода команды"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.employee_repo = TeamEmployeeRepository(session)
        self.team_repo = TeamRepository(session)

    async def add_employee(self, data: EmployeeCreate) -> TeamEmployee:
        """Добавление сотрудника по team_code"""
        team = await self.team_repo.get_team_by_team_code(data.team_code)
        if not team:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный код")
        employee = await self.employee_repo.create(employee_id=data.employee_id, team_id=team.id)
        return employee
