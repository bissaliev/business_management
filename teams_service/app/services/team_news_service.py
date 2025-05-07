from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import logger
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
        news = await self.repo.create_news(team_id, **data.model_dump())
        await self.session.commit()
        logger.info(f"Добавлена новость {news.id} в команде {team_id}")
        return news

    async def get_news(self, team_id: int, id: int) -> TeamNews:
        """Получение одной новости команды"""
        news = await self.repo.get_news(team_id, id)
        if not news:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данной новости не существует")
        return news

    async def update_news(self, team_id: int, id: int, data: TeamNewsUpdate) -> TeamNews:
        """Обновление новости команды"""
        await self._exists_team_news(team_id, id)
        news = await self.repo.update_news(team_id, id, **data.model_dump(exclude_unset=True))
        await self.session.commit()
        logger.info(f"Обновлена новость {news.id} в команде {team_id}")
        return news

    async def delete_news(self, team_id: int, id: int) -> None:
        """Удаление новости команды"""
        await self._exists_team_news(team_id, id)
        await self.repo.delete_news(team_id, id)
        await self.session.commit()
        logger.info(f"Удалена новость {id} в команде {team_id}")

    async def _exists_team(self, team_id: int) -> None:
        """Проверка на существование команды"""
        if not await self.team_repo.exists(team_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данной команды не существует")

    async def _exists_team_news(self, team_id: int, id: int) -> None:
        """Проверка на существование новости"""
        if not await self.repo.exists_news(team_id, id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данной новости не существует")
