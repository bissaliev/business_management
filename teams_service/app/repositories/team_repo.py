from sqlalchemy import select

from app.models.teams import Team
from app.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository):
    """Репозиторий команд"""

    model = Team

    async def get_team_by_team_code(self, team_code: str) -> Team:
        """Получение команды по team_code"""
        stmt = select(self.model).where(self.model.team_code == team_code)
        result = await self.session.scalars(stmt)
        return result.first()
