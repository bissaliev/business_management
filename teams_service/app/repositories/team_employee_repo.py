from sqlalchemy import insert, select

from app.models.teams import TeamEmployee
from app.repositories.base_repository import BaseRepository


class TeamEmployeeRepository(BaseRepository):
    """Репозиторий команд-сотрудников"""

    model = TeamEmployee

    async def get_team_employees(self, team_id: int) -> list[TeamEmployee]:
        """Получение сотрудников определенной команды"""
        stmt = select(self.model).where(self.model.team_id == team_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_specific_team_employee(self, team_id: int, employee_id: int) -> TeamEmployee:
        """Получение сотрудника определенной команды"""
        stmt = select(self.model).where(self.model.team_id == team_id, self.model.employee_id == employee_id)
        result = await self.session.scalars(stmt)
        return result.first()

    async def add_employee_to_team(self, team_id: int, data: dict) -> TeamEmployee:
        stmt = insert(self.model).values(team_id=team_id, **data).returning(self.model)
        result = await self.session.scalars(stmt)
        return result.first()
