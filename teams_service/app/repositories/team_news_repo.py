from sqlalchemy import delete, exists, insert, select, update

from app.models.teams import TeamNews
from app.repositories.base_repository import BaseRepository


class TeamNewsRepository(BaseRepository):
    """Репозиторий новостей команд"""

    model = TeamNews

    async def get_news_all(self, team_id) -> list[TeamNews]:
        """Получение новостей команды"""
        stmt = select(self.model).where(self.model.team_id == team_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def create_news(self, team_id: int, **data: dict) -> TeamNews:
        """Создание новостей команды"""
        stmt = insert(self.model).values(team_id=team_id, **data).returning(self.model)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_news(self, team_id: int, id: int) -> TeamNews:
        """Получение одной новости команды"""
        stmt = select(self.model).where(self.model.team_id == team_id, self.model.id == id)
        result = await self.session.scalars(stmt)
        return result.first()

    async def update_news(self, team_id: int, id: int, **data: dict) -> TeamNews:
        """Обновление новости команды"""
        stmt = (
            update(self.model)
            .where(self.model.team_id == team_id, self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def delete_news(self, team_id: int, id: int) -> bool:
        """Удаление новости команды"""
        stmt = delete(self.model).where(self.model.team_id == team_id, self.model.id == id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def exists_news(self, team_id: int, id: int) -> bool:
        """Удаление новости команды"""
        stmt = select(exists(self.model).where(self.model.team_id == team_id, self.model.id == id))
        result = await self.session.scalar(stmt)
        return result
