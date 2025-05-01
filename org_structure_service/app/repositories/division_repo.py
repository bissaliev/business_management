from sqlalchemy import delete, select

from app.models import Division
from app.repositories.base_repository import BaseRepository


class DivisionRepository(BaseRepository):
    """Репозиторий для модели Division"""

    model: type[Division] = Division

    async def get_team_divisions(self, team_id: int) -> list[Division]:
        """Получение дивизий определенной команды"""
        stmt = select(self.model).where(self.model.team_id == team_id)
        return (await self.session.scalars(stmt)).all()

    async def get_team_division(self, team_id: int, division_id: int) -> Division:
        """Получение дивизии определенной команды"""
        stmt = select(self.model).where(self.model.team_id == team_id, self.model.id == division_id)
        return (await self.session.scalars(stmt)).first()

    async def delete_division(self, team_id: int, division_id: int) -> None:
        """Удаление дивизии определенной команды"""
        stmt = delete(self.model).where(self.model.team_id == team_id, self.model.id == division_id)
        await self.session.execute(stmt)
