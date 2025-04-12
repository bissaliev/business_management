from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teams import Team
from app.repositories.team_repo import TeamRepository


class TeamService:
    """Сервис для управления командами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TeamRepository(session)

    async def get_team_by_code(self, team_code: str):
        stmt = select(Team).where(Team.team_code == team_code)
        result = await self.session.scalars(stmt)
        return result.first()

    async def _exists_team(self, team_id: int):
        """Проверка на существование команды"""
        return await self.repo.exists(team_id)

    async def create_team(self, team_data: dict):
        """Создание команды"""
        return await self.repo.create(team_data)

    async def get_teams(self) -> list[Team]:
        """Получение всех команд"""
        teams = await self.repo.get_all()
        return teams

    async def get_one(self, team_id: int) -> Team:
        """Получение одной команды"""
        return await self.repo.get(team_id)

    async def update_team(self, team_id: int, update_data: dict) -> Team:
        """Обновление данных команды"""
        if not await self.repo.exists(team_id):
            raise HTTPException(status_code=404, detail=f"Команды с таким {team_id=} не существует")
        return await self.repo.update(team_id, update_data)
