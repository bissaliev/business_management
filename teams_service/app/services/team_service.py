from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teams import Team
from app.repositories.team_repo import TeamRepository
from app.schemas.teams import TeamCreate, TeamUpdate


class TeamService:
    """Сервис для управления командами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TeamRepository(session)

    async def get_team_by_code(self, team_code: str):
        """Получение команды по специально коду"""
        return await self.repo.get_team_by_team_code(team_code)

    async def create_team(self, team_data: TeamCreate):
        """Создание команды"""
        return await self.repo.create(**team_data.model_dump())

    async def get_teams(self) -> list[Team]:
        """Получение всех команд"""
        teams = await self.repo.get_all()
        return teams

    async def get_one(self, team_id: int) -> Team:
        """Получение одной команды"""
        team = await self.repo.get(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
        return team

    async def update_team(self, team_id: int, update_data: TeamUpdate) -> Team:
        """Обновление данных команды"""
        await self._exists_team(team_id)
        return await self.repo.update(team_id, **update_data.model_dump(exclude_unset=True))

    async def delete_team(self, team_id: int) -> Team:
        """Удаление команды"""
        await self._exists_team(team_id)
        return await self.repo.delete(team_id)

    async def _exists_team(self, team_id: int) -> None:
        if not await self.repo.exists(team_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Команды с таким {team_id=} не существует"
            )
