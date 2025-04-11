from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Department
from app.repositories.department_repo import DepartmentRepository
from app.repositories.division_repo import DivisionRepository
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas.team_structures import StructureType


class DepartmentService:
    """Сервис для управления департаментами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DepartmentRepository(session)
        self.division_repo = DivisionRepository(session)
        self.team_structure_repo = TeamStructureRepository(session)

    def verify_division_type(self, structure_type, division_id):
        """Проверка на использования дивизии только в матричной орг. структуре"""
        if structure_type == StructureType.DIVISIONAL and division_id is None:
            return True
        return bool(division_id and structure_type != StructureType.DIVISIONAL)

    async def exists_division(self, division_id: int):
        """Проверка на существование дивизии"""
        return division_id and not await self.division_repo.exists(division_id)

    async def exists_department(self, parent_id: int):
        """Проверка на существование департамента"""
        return await self.repo.exists(parent_id)

    async def create_department(self, department_data: dict):
        """Создание департамента"""
        team_structure = await self.team_structure_repo.get(department_data["team_id"])
        if team_structure is None:
            raise HTTPException(status_code=404, detail="TeamStructure не существует")

        if self.verify_division_type(team_structure.structure_type, department_data["division_id"]):
            raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

        if await self.exists_division(department_data["division_id"]):
            raise HTTPException(status_code=404, detail="Division не существует")

        if department_data["parent_id"] and not await self.exists_department(department_data["parent_id"]):
            raise HTTPException(
                status_code=404, detail=f"Департамент с id={department_data['parent_id']} не существует"
            )

        try:
            department = await self.repo.add(department_data)
            return department
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e

    async def get_departments(self) -> list[Department]:
        """Получение всех департаментов"""
        departments = await self.repo.get_all()
        return departments

    async def get_department(self, department_id: int) -> Department:
        department = await self.repo.get(department_id)
        if not department:
            raise HTTPException(status_code=404, detail=f"Департамент с id={department_id} не существует")
        return department

    async def update_department(self, department_id: int, update_data: dict) -> Department:
        if not await self.repo.exists(department_id):
            raise HTTPException(status_code=404, detail=f"Департамент с id={department_id} не существует")
        try:
            return await self.repo.update(department_id, update_data)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e
