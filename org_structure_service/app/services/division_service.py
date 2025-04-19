from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Division, TeamStructure
from app.repositories.division_repo import DivisionRepository
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas.divisions import DivisionCreate, DivisionUpdate
from app.schemas.team_structures import StructureType


class DivisionService:
    """Сервис для дивизии"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DivisionRepository(session)
        self.team_structure_repo = TeamStructureRepository(session)

    async def get_divisions(self) -> list[Division]:
        """Получение всех дивизии"""
        return await self.repo.get_all()

    async def get_division(self, division_id: int) -> Division:
        """Получение дивизии"""
        division = await self.repo.get(division_id)
        if not division:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Дивизии с id={division_id} не существует"
            )
        return division

    async def create_division(self, division_data: DivisionCreate) -> Division:
        """Создание дивизии"""
        await self._get_team_structure(division_data.team_id)
        try:
            department = await self.repo.add(**division_data.model_dump())
            return department
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка  базы данных") from e

    async def update_division(self, division_id: int, update_data: DivisionUpdate) -> Division:
        """Обновление дивизии"""
        if not await self.repo.exists(division_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Дивизии с id={division_id} не существует"
            )
        if update_data.team_id:
            await self._get_team_structure()
        try:
            return await self.repo.update(division_id, **update_data.model_dump(exclude_unset=True))
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка  базы данных") from e

    async def _get_team_structure(self, team_id: int) -> TeamStructure:
        """Проверка на существование и необходимый тип структуры"""
        team_structure = await self.team_structure_repo.get(team_id)
        if team_structure is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TeamStructure не существует")
        if team_structure.structure_type != StructureType.DIVISIONAL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Дивизия определяется только для дивизионной структуры"
            )
        return team_structure
