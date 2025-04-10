from sqlalchemy import exists, select
from sqlalchemy.orm import selectinload

from app.models import Department, Division, EmployeeStructure, TeamStructure
from app.repositories.base_repository import BaseRepository


class TeamStructureRepository(BaseRepository):
    model = TeamStructure

    async def get(self, reference: int):
        stmt = select(self.model).where(self.model.team_id == reference)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_relationship_upload(self, reference: int):
        """Запрос с загрузкой всех связанных отношений"""
        stmt = (
            select(TeamStructure)
            .where(TeamStructure.team_id == reference)
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
        return team_structure

    async def exists(self, reference):
        stmt = select(exists(self.model).where(self.model.team_id == reference))
        result = await self.session.execute(stmt)
        return result.scalar()
