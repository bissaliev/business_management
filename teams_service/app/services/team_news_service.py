from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teams import TeamNews
from app.repositories.team_news_repo import TeamNewsRepository
from app.repositories.team_repo import TeamRepository
from app.schemas.team_news import TeamNewsCreate, TeamNewsUpdate


class TeamNewsService:
    """Сервис для управления новостями в команде"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.team_repo = TeamRepository(session)
        self.repo = TeamNewsRepository(session)

    async def get_news_all(self, team_id: int) -> list[TeamNews]:
        """Получение всех новостей команды"""
        await self._exists_team(team_id)
        return await self.repo.get_news_all(team_id)

    async def create_news(self, team_id: int, data: TeamNewsCreate) -> TeamNews:
        """Создание новости в команде"""
        await self._exists_team(team_id)
        return await self.repo.create_news(team_id, **data.model_dump())

    async def get_news(self, team_id: int, id: int) -> TeamNews:
        """Получение одной новости команды"""
        news = await self.repo.get_news(team_id, id)
        if not news:
            raise HTTPException(status_code=404, detail="Данной новости не существует")
        return news

    async def update_news(self, team_id: int, id: int, data: TeamNewsUpdate) -> TeamNews:
        """Обновление новости команды"""
        await self._exists_team_news(team_id, id)
        return await self.repo.update_news(team_id, id, **data.model_dump(exclude_unset=True))

    async def delete_news(self, team_id: int, id: int) -> None:
        """Удаление новости команды"""
        await self._exists_team_news(team_id, id)
        await self.repo.delete_news(team_id, id)

    async def _exists_team(self, team_id: int) -> bool:
        """Проверка на существование команды"""
        if not await self.team_repo.exists(team_id):
            raise HTTPException(status_code=404, detail="Данной команды не существует")

    async def _exists_team_news(self, team_id: int, id: int) -> bool:
        """Проверка на существование новости"""
        if not await self.repo.exists_news(team_id, id):
            raise HTTPException(status_code=404, detail="Данной новости не существует")
