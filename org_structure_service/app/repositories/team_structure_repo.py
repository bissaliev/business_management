from sqlalchemy import select

from app.models import TeamStructure
from app.repositories.base_repository import BaseRepository


class TeamStructureRepository(BaseRepository):
    model = TeamStructure

    async def get(self, reference):
        stmt = select(self.model).where(self.model.team_id == reference)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
