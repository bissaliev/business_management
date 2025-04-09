from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Department, Division, EmployeeManagers, EmployeeStructure, StructureType, TeamStructure
from app.routers.dependencies import OrgStructureServiceDeps
from app.schemas import (
    DepartmentCreate,
    DepartmentResponse,
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


@router.post("/departments/", summary="Создание отдела")
async def create_department(
    department: DepartmentCreate, session: Annotated[AsyncSession, Depends(get_session)]
) -> DepartmentResponse:
    stmt = select(TeamStructure).where(TeamStructure.team_id == department.team_id)
    result = await session.execute(stmt)
    team_structure = result.scalar_one_or_none()
    if not team_structure:
        raise HTTPException(status_code=404, detail="TeamStructure не существует")

    if team_structure.structure_type == StructureType.DIVISIONAL and department.division_id is None:
        raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

    if department.division_id and team_structure.structure_type != StructureType.DIVISIONAL:
        raise HTTPException(status_code=400, detail="division_id требуется для определения дивизионной структуры")

    if department.division_id:
        stmt = select(Division).where(Division.id == department.division_id, Division.team_id == department.team_id)
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Division не существует")

    if department.parent_department_id:
        stmt = select(Department).where(
            Department.id == department.parent_department_id, Department.team_id == department.team_id
        )
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Parent department не существует")

    db_dept = Department(**department.model_dump())
    session.add(db_dept)
    try:
        await session.commit()
    except IntegrityError as e:
        if "uq_department_team_name" in str(e):
            raise HTTPException(
                status_code=409,
                detail=f"Отдел с именем {department.name} уже существует для команды {department.team_id}",
            ) from e
        # Если это другая ошибка IntegrityError (например, foreign key), возвращаем общую ошибку
        raise HTTPException(status_code=400, detail="Database integrity error: " + str(e)) from e
    await session.refresh(db_dept)
    return db_dept


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
