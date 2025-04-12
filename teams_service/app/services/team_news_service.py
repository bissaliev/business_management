from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teams import TeamNews
from app.repositories.team_news_repo import TeamNewsRepository
from app.repositories.team_repo import TeamRepository


class TeamNewsService:
    """Сервис для управления новостями в команде"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.team_repo = TeamRepository(session)
        self.repo = TeamNewsRepository(session)

    async def get_news_all(self, team_id: int) -> list[TeamNews]:
        """Получение всех новостей команды"""
        if not await self._exists_team(team_id):
            raise HTTPException(status_code=404, detail="Данной команды не существует")
        return await self.repo.get_news_all(team_id)

    async def create_news(self, team_id: int, data: dict) -> TeamNews:
        """Создание новости в команде"""
        if not await self._exists_team(team_id):
            raise HTTPException(status_code=404, detail="Данной команды не существует")
        return await self.repo.create_news(team_id, data)

    async def get_news(self, team_id: int, id: int) -> TeamNews:
        """Получение одной новости команды"""
        news = await self.repo.get_news(team_id, id)
        if not news:
            raise HTTPException(status_code=404, detail="Данной новости не существует")
        return news

    async def update_news(self, team_id: int, id: int, data: dict) -> TeamNews:
        """Обновление новости команды"""
        if not await self._exists_team_news(team_id, id):
            raise HTTPException(status_code=404, detail="Данной новости не существует")
        return await self.repo.update_news(team_id, id, data)

    async def delete_news(self, team_id: int, id: int) -> None:
        """Удаление новости команды"""
        if not await self._exists_team_news(team_id, id):
            raise HTTPException(status_code=404, detail="Данной новости не существует")
        await self.repo.delete_news(team_id, id)

    async def _exists_team(self, team_id: int) -> bool:
        """Проверка на существование команды"""
        return await self.team_repo.exists(team_id)

    async def _exists_team_news(self, team_id: int, id: int) -> bool:
        """Проверка на существование новости"""
        return await self.repo.exists_news(team_id, id)
