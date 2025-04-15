from fastapi import APIRouter

from app.routers.dependencies import EmployeeManagerServiceDeps, EmployeeServiceDeps
from app.schemas.employees import (
    AddManager,
    EmployeeManagerCreate,
    EmployeeManagerResponse,
    EmployeeResponse,
    EmployeeStructureCreate,
    EmployeeStructureUpdate,
)

router = APIRouter()


@router.get("/", summary="Список всех сотрудников с фильтрацией по департаменту")
async def get_employees(
    employee_service: EmployeeServiceDeps, department_id: int | None = None
) -> list[EmployeeResponse]:
    employees = await employee_service.get_employees(department_id)
    return employees


@router.post("/", summary="Добавление сотрудника")
async def add_employee_to_structure(
    employee: EmployeeStructureCreate, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    new_employee = await employee_service.add_employee(employee.model_dump(exclude_unset=True))
    return new_employee


@router.get("/{employee_id}", summary="Получить работника")
async def get_one(employee_id: int, employee_service: EmployeeServiceDeps) -> EmployeeResponse:
    employee = await employee_service.get_employee(employee_id)
    return employee


@router.put("/{employee_id}", summary="Обновление данных сотрудника")
async def update_employees(
    employee_id: int, employee_data: EmployeeStructureUpdate, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    employee = await employee_service.update_employee(employee_id, employee_data.model_dump(exclude_unset=True))
    return employee


@router.delete("/{employee_id}", summary="Удаление сотрудника")
async def delete_employees(employee_id: int, employee_service: EmployeeServiceDeps) -> dict:
    await employee_service.delete_employee(employee_id)
    return {"message": "Работник удален"}


@router.post("/add_managers/", summary="Назначение руководителя сотрудникам")
async def add_manager(manager_data: AddManager, employee_service: EmployeeServiceDeps) -> dict:
    await employee_service.add_manager(**manager_data.model_dump())
    return {"message": "Руководитель назначен"}


@router.post("/add_extra_managers/", summary="Добавление дополнительного руководителя")
async def add_extra_manager(
    manager: EmployeeManagerCreate, employee_manager_service: EmployeeManagerServiceDeps
) -> EmployeeManagerResponse:
    employee_manager = await employee_manager_service.add_manager(manager.model_dump())
    return employee_manager


@router.get("/{employee_id}/department_members", summary="Список коллег департамента сотрудника")
async def get_department_members(employee_id: int, employee_service: EmployeeServiceDeps) -> list[EmployeeResponse]:
    employees = await employee_service.get_department_members(employee_id)
    return employees
