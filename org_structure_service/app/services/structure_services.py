import httpx
from fastapi import HTTPException
from sqlalchemy import exists, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models import Department, Division, EmployeeStructure, TeamStructure
from app.schemas import StructureType, TeamStructureResponse


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

    async def exists_division(self, division_id: int, team_id: int):
        """Проверка на существование дивизия"""
        stmt = select(Division).where(Division.id == division_id, Division.team_id == team_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_department(self, department_data: dict):
        """Создание департамента"""
        stmt = select(TeamStructure).where(TeamStructure.team_id == department_data["team_id"])
        result = await self.session.execute(stmt)
        team_structure = result.scalar_one_or_none()
        if not await self.exists_team_structure(department_data["team_id"]):
            raise HTTPException(status_code=404, detail="TeamStructure не существует")

        if team_structure.structure_type == StructureType.DIVISIONAL and department_data["division_id"] is None:
            raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

        if department_data["division_id"] and team_structure.structure_type != StructureType.DIVISIONAL:
            raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

        if department_data["division_id"] and not await self.exists_division(
            department_data["division_id"], department_data["team_id"]
        ):
            raise HTTPException(status_code=404, detail="Division не существует")

        if department_data["parent_department_id"]:
            stmt = select(Department).where(
                Department.id == department_data["parent_department_id"],
                Department.team_id == department_data["team_id"],
            )
            result = await self.session.execute(stmt)
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Parent department не существует")

        db_dept = Department(**department_data)
        self.session.add(db_dept)
        try:
            await self.session.commit()
        except IntegrityError as e:
            if "uq_department_team_name" in str(e):
                raise HTTPException(
                    status_code=409,
                    detail=f"Отдел с именем {department_data['name']} уже существует для команды {department_data['team_id']}",
                ) from e
            # Если это другая ошибка IntegrityError (например, foreign key), возвращаем общую ошибку
            raise HTTPException(status_code=400, detail="Database integrity error: " + str(e)) from e
        await self.session.refresh(db_dept)
        return db_dept
