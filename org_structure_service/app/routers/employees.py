from fastapi import APIRouter

from app.routers.dependencies import EmployeeManagerServiceDeps, EmployeeServiceDeps
from app.schemas.employees import (
    EmployeeManagerCreate,
    EmployeeManagerResponse,
    EmployeeResponse,
    EmployeeStructureCreate,
    EmployeeStructureUpdate,
)

router = APIRouter()


@router.get("/", summary="Список всех сотрудников")
async def get_employees(employee_service: EmployeeServiceDeps) -> list[EmployeeResponse]:
    employees = await employee_service.get_employees()
    return employees


@router.post("/", summary="Добавление сотрудника")
async def add_employee_to_structure(
    employee: EmployeeStructureCreate, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    new_employee = await employee_service.add_employee(employee.model_dump(exclude_unset=True))
    return new_employee


@router.get("/{id}", summary="Получить работника")
async def get_one(id: int, employee_service: EmployeeServiceDeps) -> EmployeeResponse:
    employee = await employee_service.get_employee(id)
    return employee


@router.get("/{department_id}", summary="Список сотрудников определенного департамента")
async def get_department_employees(
    department_id: int, employee_service: EmployeeServiceDeps
) -> list[EmployeeResponse]:
    employees = await employee_service.get_department_employees(department_id)
    return employees


@router.put("/{id}", summary="Обновление данных сотрудника")
async def update_employees(
    id: int, employee_data: EmployeeStructureUpdate, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    employee = await employee_service.update_employee(id, employee_data.model_dump(exclude_unset=True))
    return employee


@router.post("/managers/", summary="Добавление дополнительного руководителя")
async def add_employee_manager(
    manager: EmployeeManagerCreate, employee_manager_service: EmployeeManagerServiceDeps
) -> EmployeeManagerResponse:
    employee_manager = await employee_manager_service.add_manager(manager.model_dump())
    return employee_manager
