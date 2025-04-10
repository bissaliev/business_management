from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import EmployeeManagers, EmployeeStructure
from app.routers.dependencies import OrgStructureServiceDeps
from app.schemas import (
    EmployeeManagerCreate,
    EmployeeStructureCreate,
    TeamStructureCreate,
    TeamStructureResponse,
    TeamStructureResponseShort,
)

router = APIRouter()


@router.post("/team-structure/", summary="Создание типа структуры команды")
async def set_team_structure(
    structure: TeamStructureCreate, org_structure_service: OrgStructureServiceDeps
) -> TeamStructureResponseShort:
    new_team_structure = await org_structure_service.create_team_structure(structure.model_dump())
    return new_team_structure


@router.post("/structure/", summary="Добавление сотрудника")
async def add_employee_to_structure(
    structure: EmployeeStructureCreate, session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    db_emp = EmployeeStructure(
        employee_id=structure.employee_id,
        department_id=structure.department_id,
        role=structure.role,
        manager_id=structure.manager_id,
    )
    session.add(db_emp)
    await session.commit()
    await session.refresh(db_emp)
    return {"id": db_emp.id, "employee_id": db_emp.employee_id}


@router.post("/employee-managers/", summary="Добавление дополнительного руководителя")
async def add_employee_manager(
    manager: EmployeeManagerCreate, session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    db_mgr = EmployeeManagers(
        employee_structure_id=manager.employee_structure_id, manager_id=manager.manager_id, context=manager.context
    )
    session.add(db_mgr)
    await session.commit()
    return {"message": "Manager added"}


@router.get("/structure/{team_id}", summary="Получение иерархии")
async def get_team_structure(team_id: int, org_structure_service: OrgStructureServiceDeps) -> TeamStructureResponse:
    hierarchy = await org_structure_service.get_team_structure(team_id)
    return hierarchy


@router.get("/structure/", summary="Получение организационных структур")
async def get_team_structure_all(org_structure_service: OrgStructureServiceDeps) -> list[TeamStructureResponseShort]:
    team_structures = await org_structure_service.get_team_structure_all()
    return team_structures
