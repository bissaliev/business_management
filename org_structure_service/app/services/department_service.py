from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.department_repo import DepartmentRepository
from app.repositories.division_repo import DivisionRepository
from app.repositories.team_structure_repo import TeamStructureRepository
from app.schemas import StructureType


class DepartmentService:
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

    async def exists_parent(self, parent_id: int, team_id: int):
        """Проверка на существование департамента в team_id"""
        return await self.repo.parent_exists(parent_id, team_id)

    async def create_department(self, department_data: dict):
        """Создание департамента"""
        team_structure = await self.team_structure_repo.get(department_data["team_id"])
        if team_structure is None:
            raise HTTPException(status_code=404, detail="TeamStructure не существует")

        if self.verify_division_type(team_structure.structure_type, department_data["division_id"]):
            raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

        if await self.exists_division(department_data["division_id"]):
            raise HTTPException(status_code=404, detail="Division не существует")

        if department_data["parent_id"] and await self.exists_parent(
            department_data["parent_id"], department_data["team_id"]
        ):
            raise HTTPException(status_code=404, detail="Parent department не существует")

        try:
            db_dept = await self.repo.add(department_data)
        except IntegrityError as e:
            if "uq_department_team_name" in str(e):
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Департамент с именем {department_data['name']} "
                        f"уже существует для команды {department_data['team_id']}"
                    ),
                ) from e
            raise HTTPException(status_code=400, detail="Database integrity error: " + str(e)) from e
        await self.session.refresh(db_dept)
        return db_dept
