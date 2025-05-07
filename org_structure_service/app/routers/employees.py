from fastapi import APIRouter, status

from app.routers.dependencies import AdminAndAssignedDepartmentDeps, EmployeeServiceDeps
from app.schemas.employees import (
    AddManager,
    EmployeeManagerCreate,
    EmployeeManagerResponse,
    EmployeeResponse,
    EmployeeStructureCreate,
    EmployeeStructureUpdate,
)

router = APIRouter()


@router.get(
    "/{department_id}/employees", response_model=list[EmployeeResponse], summary="Список всех сотрудников департамента"
)
async def get_employees(department_id: int, employee_service: EmployeeServiceDeps) -> list[EmployeeResponse]:
    employees = await employee_service.get_employees(department_id)
    return employees


@router.post(
    "/{department_id}/employees",
    response_model=EmployeeResponse,
    dependencies=[AdminAndAssignedDepartmentDeps],
    summary="Добавление сотрудника",
)
async def add_employee_to_department(
    department_id: int, employee: EmployeeStructureCreate, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    new_employee = await employee_service.add_employee(department_id, employee)
    return new_employee


@router.get("/{department_id}/employees/{employee_id}", response_model=EmployeeResponse, summary="Получить работника")
async def get_department_employee(
    department_id: int, employee_id: int, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    employee = await employee_service.get_employee(department_id, employee_id)
    return employee


@router.put(
    "/{department_id}/employees/{employee_id}",
    dependencies=[AdminAndAssignedDepartmentDeps],
    response_model=EmployeeResponse,
    summary="Обновление данных сотрудника",
)
async def update_employee_position(
    department_id: int, employee_id: int, employee_data: EmployeeStructureUpdate, employee_service: EmployeeServiceDeps
) -> EmployeeResponse:
    employee = await employee_service.update_position(department_id, employee_id, employee_data)
    return employee


@router.delete(
    "/{department_id}/employees/{employee_id}",
    dependencies=[AdminAndAssignedDepartmentDeps],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление сотрудника",
)
async def delete_employees(department_id: int, employee_id: int, employee_service: EmployeeServiceDeps) -> None:
    await employee_service.delete_employee(department_id, employee_id)


@router.post(
    "/{department_id}/add_manager/",
    dependencies=[AdminAndAssignedDepartmentDeps],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Назначение руководителя сотрудникам",
)
async def add_manager(department_id: int, manager_data: AddManager, employee_service: EmployeeServiceDeps) -> None:
    await employee_service.add_manager(department_id, manager_data)


@router.post(
    "/{department_id}/employees/{employee_id}/add_extra_manager/",
    dependencies=[AdminAndAssignedDepartmentDeps],
    response_model=EmployeeManagerResponse,
    summary="Добавление дополнительного руководителя",
)
async def add_extra_manager(
    department_id: int, employee_id: int, data: EmployeeManagerCreate, employee_manager_service: EmployeeServiceDeps
) -> EmployeeManagerResponse:
    employee_manager = await employee_manager_service.add_extra_manager(department_id, employee_id, data)
    return employee_manager


@router.get(
    "/{employee_id}/department_members",
    response_model=list[EmployeeResponse],
    summary="Список коллег департамента сотрудника",
)
async def get_department_members(employee_id: int, employee_service: EmployeeServiceDeps) -> list[EmployeeResponse]:
    employees = await employee_service.get_department_members(employee_id)
    return employees
