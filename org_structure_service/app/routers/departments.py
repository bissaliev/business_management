from fastapi import APIRouter

from app.routers.dependencies import AdminAndAssigned, DepartmentServiceDeps
from app.schemas.departments import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.schemas.response import MessageDelete

router = APIRouter()


@router.get("/{team_id}/departments", summary="Получение списка отделов определенной команды")
async def get_departments(team_id: int, department_service: DepartmentServiceDeps) -> list[DepartmentResponse]:
    return await department_service.get_departments(team_id)


@router.post("/{team_id}/departments", dependencies=[AdminAndAssigned], summary="Создание отдела")
async def create_department(
    team_id: int, department: DepartmentCreate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    new_department = await department_service.create_department(team_id, department)
    return new_department


@router.get("/{team_id}/departments/{department_id}", summary="Получение отдела")
async def get_department(
    team_id: int, department_id: int, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    return await department_service.get_department(team_id, department_id)


@router.patch("/{team_id}/departments/{department_id}", dependencies=[AdminAndAssigned], summary="Обновление отдела")
async def update_department(
    team_id: int, department_id: int, update_data: DepartmentUpdate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    return await department_service.update_department(team_id, department_id, update_data)


@router.delete("/{team_id}/departments/{department_id}", dependencies=[AdminAndAssigned], summary="Удаление отдела")
async def delete_department(
    team_id: int, department_id: int, department_service: DepartmentServiceDeps
) -> MessageDelete:
    await department_service.delete_department(team_id, department_id)
    return MessageDelete()
