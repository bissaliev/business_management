from fastapi import APIRouter, status

from app.routers.dependencies import AdminAndAssigned, DepartmentServiceDeps
from app.schemas.departments import DepartmentCreate, DepartmentResponse, DepartmentUpdate

router = APIRouter()


@router.get(
    "/{team_id}/departments",
    response_model=list[DepartmentResponse],
    summary="Получение списка отделов определенной команды",
)
async def get_departments(team_id: int, department_service: DepartmentServiceDeps) -> list[DepartmentResponse]:
    return await department_service.get_departments(team_id)


@router.post(
    "/{team_id}/departments",
    dependencies=[AdminAndAssigned],
    response_model=DepartmentResponse,
    summary="Создание отдела",
)
async def create_department(
    team_id: int, department: DepartmentCreate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    new_department = await department_service.create_department(team_id, department)
    return new_department


@router.get("/{team_id}/departments/{department_id}", response_model=DepartmentResponse, summary="Получение отдела")
async def get_department(
    team_id: int, department_id: int, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    return await department_service.get_department(team_id, department_id)


@router.patch(
    "/{team_id}/departments/{department_id}",
    dependencies=[AdminAndAssigned],
    response_model=DepartmentResponse,
    summary="Обновление отдела",
)
async def update_department(
    team_id: int, department_id: int, update_data: DepartmentUpdate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    return await department_service.update_department(team_id, department_id, update_data)


@router.delete(
    "/{team_id}/departments/{department_id}",
    dependencies=[AdminAndAssigned],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление отдела",
)
async def delete_department(team_id: int, department_id: int, department_service: DepartmentServiceDeps) -> None:
    await department_service.delete_department(team_id, department_id)
