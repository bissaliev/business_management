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

    async def get_divisions(self, team_id: int) -> list[Division]:
        """Получение всех дивизии"""
        await self._get_team_or_404(team_id)
        return await self.repo.get_team_divisions(team_id)

    async def get_division(self, team_id: int, division_id: int) -> Division:
        """Получение дивизии"""
        await self._get_team_or_404(team_id)
        division = await self.repo.get(division_id)
        if not division:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Дивизии с id={division_id} не существует"
            )
        return division

    async def create_division(self, team_id: int, division_data: DivisionCreate) -> Division:
        """Создание дивизии"""
        await self._get_team_structure(team_id)
        try:
            department = await self.repo.add(team_id=team_id, **division_data.model_dump())
            return department
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка  базы данных") from e

    async def update_division(self, team_id: int, division_id: int, update_data: DivisionUpdate) -> Division:
        """Обновление дивизии"""
        await self._get_team_or_404(team_id)
        await self._get_division_or_404(team_id, division_id)
        try:
            return await self.repo.update(division_id, **update_data.model_dump(exclude_unset=True))
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка  базы данных") from e

    async def delete_division(self, team_id: int, division_id: int) -> None:
        """Удаление дивизии"""
        await self._get_team_or_404(team_id)
        await self._get_division_or_404(team_id, division_id)
        await self.repo.delete_division(team_id, division_id)

    async def _get_team_or_404(self, team_id: int) -> TeamStructure:
        """Получить команду либо вызвать ошибку 404"""
        team = await self.team_structure_repo.get(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Команда с {team_id=} не существует")
        return team

    async def _get_division_or_404(self, team_id: int, division_id: int) -> Division:
        """Получить дивизию либо вызвать ошибку 404"""
        division = await self.repo.get_team_division(team_id, division_id)
        if not division:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Дивизия с {division_id=} не существует"
            )
        return division

    async def _get_team_structure(self, team_id: int) -> TeamStructure:
        """Проверка на существование и необходимый тип структуры"""
        team_structure = await self._get_team_or_404(team_id)
        if team_structure.structure_type != StructureType.DIVISIONAL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Дивизия определяется только для дивизионной структуры"
            )
        return team_structure
