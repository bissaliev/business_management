from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Department, Division, EmployeeStructure, TeamStructure
from app.schemas import TeamStructureResponse


class OrgStructureService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team_structure_all(self):
        result = await self.session.scalars(select(TeamStructure))
        return result.all()

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
