from sqlalchemy import delete, exists, select, update

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

    async def exists_employee_team(self, team_id: int, employee_id: int) -> bool:
        """Проверка на существование работника в команде"""
        stmt = select(exists(self.model).where(self.model.team_id == team_id, self.model.employee_id == employee_id))
        result = await self.session.scalar(stmt)
        return result

    async def update_role(self, team_id: int, employee_id: int, role: dict) -> TeamEmployee:
        """Обновление роли работника команды"""
        stmt = (
            update(self.model)
            .where(self.model.team_id == team_id, self.model.employee_id == employee_id)
            .values(**role)
            .returning(self.model)
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def delete_employee(self, team_id: int, employee_id: int) -> bool:
        """Удаление роли работника команды"""
        stmt = delete(self.model).where(self.model.team_id == team_id, self.model.employee_id == employee_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
