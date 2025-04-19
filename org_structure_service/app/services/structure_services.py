from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models import TeamStructure
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas.team_structures import TeamStructureCreate, TeamStructureResponse


class OrgStructureService:
    """Сервис Организационной структуры команды"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TeamStructureRepository(session)
        self.team_client = TeamServiceClient()

    async def get_team_structure_all(self) -> list[TeamStructure]:
        """Получение всех зарегистрированных организационных структур"""
        team_structures = await self.repo.get_all()
        return team_structures

    async def create_team_structure(self, structure_data: TeamStructureCreate) -> TeamStructure:
        """Создание организационной структуры команды"""
        team = await self._get_team_on_team_service(structure_data.team_id)
        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Команда с id={structure_data.team_id} еще не зарегистрирована",
            )
        if await self.repo.exists(structure_data.team_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Структура команды с team_id={structure_data.team_id} уже существует",
            )
        team_structure = await self.repo.add(**structure_data.model_dump())
        return team_structure

    async def get_team_structure(self, team_id: int) -> TeamStructureResponse:
        """Получение структуры команды с иерархией департаментов и дивизий"""
        team_structure = await self.repo.get_with_relationship_upload(team_id)

        if not team_structure:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Структура команды с team_id={team_id} не существует"
            )

        return TeamStructureResponse.model_validate(team_structure)

    async def _get_team_on_team_service(self, team_id: int) -> TeamStructure:
        """Проверка на существование команды в team_service"""
        team = await self.team_client.get_team(team_id)
        return team
