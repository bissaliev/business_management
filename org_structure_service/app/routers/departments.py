from fastapi import APIRouter

from app.routers.dependencies import DepartmentServiceDeps
from app.schemas.departments import DepartmentCreate, DepartmentResponse, DepartmentUpdate

router = APIRouter()


@router.get("/", summary="Получение списка всех отделов")
async def get_departments(department_service: DepartmentServiceDeps) -> list[DepartmentResponse]:
    return await department_service.get_departments()


@router.post("/", summary="Создание отдела")
async def create_department(
    department: DepartmentCreate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    new_department = await department_service.create_department(department.model_dump())
    return new_department


@router.get("/{id}", summary="Получение отдела")
async def get_department(id: int, department_service: DepartmentServiceDeps) -> DepartmentResponse:
    return await department_service.get_department(id)


@router.put("/{id}", summary="Обновление отдела")
async def update_department(
    id: int, update_data: DepartmentUpdate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    return await department_service.update_department(id, update_data.model_dump(exclude_unset=True))
