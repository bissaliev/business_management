from fastapi import APIRouter

from app.routers.dependencies import DepartmentServiceDeps
from app.schemas.departments import (
    DepartmentCreate,
    DepartmentResponse,
)

router = APIRouter()


@router.post("/", summary="Создание отдела")
async def create_department(
    department: DepartmentCreate, department_service: DepartmentServiceDeps
) -> DepartmentResponse:
    new_department = await department_service.create_department(department.model_dump())
    return new_department
