import httpx
from fastapi import HTTPException
from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models import Department, Division, EmployeeStructure, TeamStructure
from app.schemas import TeamStructureResponse


class OrgStructureService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team_structure_all(self):
        result = await self.session.scalars(select(TeamStructure))
        return result.all()

    async def exists_team_on_team_service(self, team_id: int):
        base_team_url = settings.get_team_service__url()
        url = f"{base_team_url}/{team_id}/"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code != 200:
                    return None
                return response.json()
        except httpx.ConnectError:
            return True

    async def exists_team_structure(self, team_id: int):
        stmt = select(exists().where(TeamStructure.team_id == team_id))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_team_structure(self, structure_data: dict):
        team_id = structure_data["team_id"]
        is_exists_team = await self.exists_team_on_team_service(team_id)
        if is_exists_team is None:
            raise HTTPException(status_code=404, detail=f"Команда с id={team_id} еще не зарегистрирована")
        if await self.exists_team_structure(team_id):
            raise HTTPException(status_code=400, detail=f"Структура команды с id={team_id} уже существует")
        stmt = insert(TeamStructure).values(**structure_data).returning(TeamStructure)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_team_structure(self, team_id: int) -> TeamStructureResponse:
        # Запрос с загрузкой всех связанных данных
        stmt = (
            select(TeamStructure)
            .where(TeamStructure.team_id == team_id)
            .options(
                # Загружаем divisions и их departments
                selectinload(TeamStructure.divisions)
                .selectinload(Division.departments)
                .options(
                    selectinload(Department.employees).selectinload(EmployeeStructure.extra_managers),
                    selectinload(Department.children),  # Рекурсивно загружаем дочерние отделы
                ),
                # Загружаем departments напрямую
                selectinload(TeamStructure.departments).options(
                    selectinload(Department.employees).selectinload(EmployeeStructure.extra_managers),
                    selectinload(Department.children),  # Рекурсивно загружаем дочерние отделы
                ),
            )
        )
        result = await self.session.execute(stmt)
        team_structure = result.scalar_one_or_none()

        if not team_structure:
            return TeamStructureResponse(team_id=team_id, structure_type="linear", divisions=[], departments=[])

        return TeamStructureResponse.model_validate(team_structure)
