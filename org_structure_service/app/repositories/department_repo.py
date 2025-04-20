from sqlalchemy import select

from app.models import Department
from app.repositories.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    """Репозиторий для модели Department"""

    model = Department

    async def get_team_departments(self, team_id: int) -> list[Department]:
        """Получение департаментов определенной команды"""
        stmt = select(self.model).where(self.model.team_id == team_id)
        return (await self.session.scalars(stmt)).all()

    async def get_team_department(self, team_id: int, department_id: int) -> Department:
        """Получение департаментов определенной команды"""
        stmt = select(self.model).where(self.model.team_id == team_id, self.model.id == department_id)
        return (await self.session.scalars(stmt)).first()
