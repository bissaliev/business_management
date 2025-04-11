from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas.team_structures import TeamStructureResponse


class OrgStructureService:
    """Сервис Организационной структуры команды"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TeamStructureRepository(session)
        self.team_client = TeamServiceClient()

    async def get_team_structure_all(self):
        team_structures = await self.repo.get_all()
        return team_structures

    # TODO: Поправить правильную обработку запросов httpx.AsyncClient
    async def get_team_on_team_service(self, team_id: int):
        """Проверка на существование команды в team_service"""
        team = await self.team_client.get_team(team_id)
        return team

    # TODO: Подумать о том чтобы создавать команду на этом сервисе в момент создания в team service
    async def create_team_structure(self, structure_data: dict):
        """Создание организационной структуры команды"""
        team_id = structure_data["team_id"]
        team = await self.get_team_on_team_service(team_id)
        if team is None:
            raise HTTPException(status_code=404, detail=f"Команда с id={team_id} еще не зарегистрирована")
        if await self.repo.exists(team_id):
            raise HTTPException(status_code=400, detail=f"Структура команды с team_id={team_id} уже существует")
        team_structure = await self.repo.add(structure_data)
        return team_structure

    async def get_team_structure(self, team_id: int) -> TeamStructureResponse:
        """Получение структуры команды с иерархией департаментов и дивизий"""
        team_structure = await self.repo.get_with_relationship_upload(team_id)

        if not team_structure:
            raise HTTPException(status_code=400, detail=f"Структура команды с team_id={team_id} не существует")

        return TeamStructureResponse.model_validate(team_structure)
