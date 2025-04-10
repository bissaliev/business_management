from sqlalchemy import select

from app.models import Department
from app.repositories.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    model = Department

    async def parent_exists(self, parent_id: int, team_id: int):
        stmt = select(Department).where(
            Department.id == parent_id,
            Department.team_id == team_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
