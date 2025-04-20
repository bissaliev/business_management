from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Department
from app.repositories.department_repo import DepartmentRepository
from app.repositories.division_repo import DivisionRepository
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas.departments import DepartmentCreate, DepartmentUpdate
from app.schemas.team_structures import StructureType


class DepartmentService:
    """Сервис для управления департаментами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DepartmentRepository(session)
        self.division_repo = DivisionRepository(session)
        self.team_structure_repo = TeamStructureRepository(session)

    async def create_department(self, team_id: int, department_data: DepartmentCreate):
        """Создание департамента"""
        team_structure = await self._get_team_or_404(team_id)

        if self._verify_division_type(team_structure.structure_type, department_data.division_id):
            raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

        if department_data.division_id:
            await self._get_division_or_404(department_data.division_id)

        if department_data.parent_id:
            await self._get_department_or_404(team_id, department_data.parent_id)

        try:
            department = await self.repo.add(team_id=team_id, **department_data.model_dump())
            return department
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e

    async def get_departments(self, team_id: int) -> list[Department]:
        """Получение департаментов определенной команды"""
        await self._get_team_or_404(team_id)
        departments = await self.repo.get_team_departments(team_id)
        return departments

    async def get_department(self, team_id: int, department_id: int) -> Department:
        """Получение департамента"""
        await self._get_team_or_404(team_id)
        return await self._get_department_or_404(team_id, department_id)

    async def update_department(self, team_id: int, department_id: int, update_data: DepartmentUpdate) -> Department:
        """Обновление департамента"""
        team_structure = await self._get_team_or_404(team_id)
        await self._get_department_or_404(team_id, department_id)
        if self._verify_division_type(team_structure.structure_type, update_data.division_id):
            raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")
        if update_data.division_id:
            await self._get_division_or_404(update_data.division_id)

        if update_data.parent_id:
            await self._get_department_or_404(team_id, update_data.parent_id)
        try:
            return await self.repo.update(department_id, **update_data.model_dump(exclude_unset=True))
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e

    async def delete_department(self, team_id: int, department_id: int) -> Department:
        """Удаление департамента"""
        await self._get_team_or_404(team_id)
        await self._get_department_or_404(team_id, department_id)
        try:
            return await self.repo.delete_department(team_id, department_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e

    def _verify_division_type(self, structure_type, division_id):
        """Проверка на использования дивизии только в матричной орг. структуре"""
        if structure_type == StructureType.DIVISIONAL and division_id is None:
            return True
        return bool(division_id and structure_type != StructureType.DIVISIONAL)

    async def _get_department_or_404(self, team_id: int, department_id: int):
        """Получить департамент либо вызвать ошибку 404"""
        department = await self.repo.get_team_department(team_id, department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Департамент с {department_id=} не существует"
            )
        return department

    async def _get_team_or_404(self, team_id: int):
        """Получить команду либо вызвать ошибку 404"""
        team = await self.team_structure_repo.get(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Команда с {team_id=} не существует")
        return team

    async def _get_division_or_404(self, division_id: int):
        """Получить дивизию либо вызвать ошибку 404"""
        division = await self.division_repo.get(division_id)
        if not division:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Дивизия с {division_id=} не существует"
            )
        return division
