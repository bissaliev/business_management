from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Department, EmployeeManagers, EmployeeStructure, TeamStructure
from app.schemas import DepartmentCreate, EmployeeManagerCreate, EmployeeStructureCreate, TeamStructureCreate

router = APIRouter()


@router.post("/team-structure/", summary="Создание типа структуры команды")
async def set_team_structure(
    structure: TeamStructureCreate, session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    db_structure = TeamStructure(team_id=structure.team_id, structure_type=structure.structure_type)
    session.add(db_structure)
    await session.commit()
    return {"team_id": structure.team_id, "structure_type": structure.structure_type}


@router.post("/departments/", summary="Создание отдела")
async def create_department(
    department: DepartmentCreate, session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    db_dept = Department(
        team_id=department.team_id, name=department.name, parent_department_id=department.parent_department_id
    )
    session.add(db_dept)
    await session.commit()
    await session.refresh(db_dept)
    return {"id": db_dept.id, "team_id": db_dept.team_id, "name": db_dept.name}


@router.post("/structure/", summary="Добавление сотрудника")
async def add_employee_to_structure(
    structure: EmployeeStructureCreate, session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    db_emp = EmployeeStructure(
        user_id=structure.user_id,
        department_id=structure.department_id,
        role=structure.role,
        manager_id=structure.manager_id,
    )
    session.add(db_emp)
    await session.commit()
    await session.refresh(db_emp)
    return {"id": db_emp.id, "user_id": db_emp.user_id}


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


@router.get("/structure/{team_id}", response_model=dict, summary="Получение иерархии")
async def get_team_structure(team_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    # Тип структуры
    result = await session.execute(select(TeamStructure).where(TeamStructure.team_id == team_id))
    structure = result.scalar_one_or_none()
    structure_type = structure.structure_type if structure else "linear"

    # Отделы
    result = await session.execute(Department.__table__.select().where(Department.team_id == team_id))
    departments = [{"id": row.id, "name": row.name, "parent_id": row.parent_department_id} for row in result]

    # Сотрудники
    result = await session.execute(
        EmployeeStructure.__table__.select().where(EmployeeStructure.department_id.in_([d["id"] for d in departments]))
    )
    employees = [
        {
            "id": row.id,
            "user_id": row.user_id,
            "dept_id": row.department_id,
            "role": row.role,
            "manager_id": row.manager_id,
        }
        for row in result
    ]

    # Дополнительные руководители
    result = await session.execute(
        EmployeeManagers.__table__.select().where(
            EmployeeManagers.employee_structure_id.in_([e["id"] for e in employees])
        )
    )
    extra_managers = [
        {"emp_id": row.employee_structure_id, "manager_id": row.manager_id, "context": row.context} for row in result
    ]

    # Построение иерархии
    hierarchy = build_hierarchy(departments, employees, extra_managers, structure_type)
    return {"structure_type": structure_type, "hierarchy": hierarchy}


def build_hierarchy(
    departments: list[dict], employees: list[dict], extra_managers: list[dict], structure_type: str
) -> dict:
    """Вспомогательная функция для построения иерархии"""
    dept_map = {dept["id"]: {"name": dept["name"], "children": [], "employees": []} for dept in departments}
    emp_map = {
        emp["id"]: {
            "user_id": emp["user_id"],
            "role": emp["role"],
            "managers": [emp["manager_id"]] if emp["manager_id"] else [],
        }
        for emp in employees
    }

    for mgr in extra_managers:
        if mgr["emp_id"] in emp_map:
            emp_map[mgr["emp_id"]]["managers"].append({"manager_id": mgr["manager_id"], "context": mgr["context"]})

    for emp in employees:
        dept_id = emp["dept_id"]
        if dept_id in dept_map:
            dept_map[dept_id]["employees"].append(emp_map[emp["id"]])

    root_depts = []
    for dept in departments:
        parent_id = dept["parent_id"]
        if parent_id is None:
            root_depts.append(dept_map[dept["id"]])
        else:
            if parent_id in dept_map:
                dept_map[parent_id]["children"].append(dept_map[dept["id"]])

    return {"departments": root_depts if structure_type != "matrix" else dept_map, "employees": emp_map}
