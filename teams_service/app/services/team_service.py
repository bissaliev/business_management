from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import logger
from app.models.teams import Team
from app.repositories.team_repo import TeamRepository
from app.schemas.teams import TeamUpdate


class TeamService:
    """Сервис для управления командами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TeamRepository(session)

    async def get_team_by_code(self, team_code: str) -> Team:
        """Получение команды по специально коду"""
        return await self.repo.get_team_by_team_code(team_code)

    async def get_one(self, team_id: int) -> Team:
        """Получение одной команды"""
        team = await self.repo.get(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
        return team

    async def update_team(self, team_id: int, update_data: TeamUpdate) -> Team:
        """Обновление данных команды"""
        await self._exists_team(team_id)
        team = await self.repo.update(team_id, **update_data.model_dump(exclude_unset=True))
        await self.session.commit()
        logger.info(f"Обновлена команда {team_id}")
        return team

    async def delete_team(self, team_id: int) -> None:
        """Удаление команды"""
        await self._exists_team(team_id)
        await self.repo.delete(team_id)
        await self.session.commit()
        logger.info(f"Удалена команда {team_id}")

    async def _exists_team(self, team_id: int) -> None:
        if not await self.repo.exists(team_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Команды с таким {team_id=} не существует"
            )
