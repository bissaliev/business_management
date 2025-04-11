from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Division
from app.repositories.division_repo import DivisionRepository
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas.team_structures import StructureType


class DivisionService:
    """Сервис для дивизии"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DivisionRepository(session)
        self.team_structure_repo = TeamStructureRepository(session)

    def verify_team_structure_type(self, structure_type) -> bool:
        """Проверка на использования дивизии только в матричной орг. структуре"""
        return structure_type == StructureType.DIVISIONAL

    async def exists_division(self, division_id: int) -> bool:
        """Проверка на существование дивизии"""
        return await self.repo.exists(division_id)

    async def get_team_structure(self, team_id: int):
        return await self.team_structure_repo.get(team_id)

    async def create_division(self, division_data: dict) -> Division:
        """Создание дивизии"""
        team_structure = await self.get_team_structure(division_data["team_id"])
        if team_structure is None:
            raise HTTPException(status_code=404, detail="TeamStructure не существует")

        if not self.verify_team_structure_type(team_structure.structure_type):
            raise HTTPException(status_code=400, detail="Дивизия определяется только для дивизионной структуры")

        try:
            department = await self.repo.add(division_data)
            return department
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e

    async def get_divisions(self) -> list[Division]:
        """Получение всех дивизии"""
        divisions = await self.repo.get_all()
        return divisions

    async def get_division(self, division_id: int) -> Division:
        division = await self.repo.get(division_id)
        if not division:
            raise HTTPException(status_code=404, detail=f"Дивизии с id={division_id} не существует")
        return division

    async def update_division(self, division_id: int, update_data: dict) -> Division:
        """Обновление дивизии"""
        if not await self.repo.exists(division_id):
            raise HTTPException(status_code=404, detail=f"Дивизии с id={division_id} не существует")
        if "team_id" in update_data:
            team_structure = await self.get_team_structure(update_data["team_id"])
            if team_structure is None:
                raise HTTPException(status_code=404, detail="TeamStructure не существует")

            if not self.verify_team_structure_type(team_structure.structure_type):
                raise HTTPException(status_code=400, detail="Дивизия определяется только для дивизионной структуры")
        try:
            return await self.repo.update(division_id, update_data)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Ошибка  базы данных") from e
