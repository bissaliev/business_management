from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models import EmployeeManagers, EmployeeRole, EmployeeStructure
from app.repositories.department_repo import DepartmentRepository
from app.repositories.employee_manager_repo import EmployeeManagerRepository
from app.repositories.employee_repo import EmployeeRepository
from app.schemas.employees import AddManager, EmployeeManagerCreate, EmployeeStructureCreate, EmployeeStructureUpdate


class EmployeeService:
    """Сервис Организационной структуры команды"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeRepository(session)
        self.extra_manager_repo = EmployeeManagerRepository(session)
        self.department_repo = DepartmentRepository(session)
        self.team_client = TeamServiceClient()

    async def add_employee(self, department_id: int, employee_data: EmployeeStructureCreate) -> EmployeeStructure:
        """Добавление работника в организационную структуру"""
        department = await self._get_department_or_404(department_id)
        if await self.repo.exists_in_department(employee_data.employee_id, department_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Работник уже зарегистрирован в данном департаменте"
            )
        await self._get_employee_from_team_service_or_404(department.team_id, employee_data.employee_id)
        try:
            employee = await self.repo.add(department_id=department_id, **employee_data.model_dump())
            return employee
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    async def update_position(
        self, department_id: int, employee_id: int, employee_data: EmployeeStructureUpdate
    ) -> EmployeeStructure:
        """Обновление позиции работника"""
        await self._get_department_or_404(department_id)
        await self.employee_in_department__or_404(department_id, employee_id)
        try:
            return await self.repo.update_employee(employee_id, **employee_data.model_dump())
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    async def get_employees(self, department_id: int) -> list[EmployeeStructure]:
        """Получить список всех сотрудников"""
        await self._get_department_or_404(department_id)
        return await self.repo.get_employees_by_department_id(department_id)

    async def get_employee(self, department_id: int, employee_id: int) -> EmployeeStructure:
        """Получить сотрудника"""
        await self._get_department_or_404(department_id)
        employee = await self.repo.get_employee(department_id, employee_id)
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Работника не существует в организационной структуре"
            )
        return employee

    async def delete_employee(self, department_id: int, employee_id: int):
        """Удаление работника"""
        await self.employee_in_department__or_404(department_id, employee_id)
        try:
            return await self.repo.delete_employee(employee_id, department_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    async def get_department_members(self, employee_id: int) -> list[EmployeeStructure]:
        """Получить всех коллег департамента сотрудника"""
        employee = await self.repo.get_employee(employee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работника не существует")
        members = await self.repo.get_employees_by_department_id(employee.department_id)
        return members

    async def add_manager(self, department_id: int, data: AddManager) -> None:
        """Назначение руководителя отдела"""
        department = await self._get_department_or_404(department_id)
        employee = await self._get_employee_from_team_service_or_404(department.team_id, data.manager_id)
        if employee.role != EmployeeRole.MANAGER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Данный работник не является менеджером"
            )
        try:
            await self.repo.add_manager(department_id, **data.model_dump())
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    async def add_extra_manager(
        self, department_id: int, employee_id: int, data: EmployeeManagerCreate
    ) -> EmployeeManagers:
        """Добавление дополнительного руководителя для сотрудника"""
        department = await self._get_department_or_404(department_id)
        employee = await self._get_employee_from_team_service_or_404(department.team_id, data.manager_id)
        if employee.role != EmployeeRole.MANAGER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Данный работник не является менеджером"
            )

        employee_structure = await self.get_employee(department_id, employee_id)
        try:
            emp_man = await self.extra_manager_repo.add(
                employee_structure_id=employee_structure.id, **data.model_dump()
            )
            return emp_man
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    async def _get_department_or_404(self, department_id: int):
        """Проверка на существование департамента"""
        department = await self.department_repo.get(department_id)
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Департамент не существует")
        return department

    async def _get_employee_from_team_service_or_404(self, team_id: int, user_id: int):
        """Проверка на существование работника в команде team_service"""
        employee = await self.team_client.get_employee(team_id, user_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Данного работника не существует в команде"
            )
        return employee

    async def employee_in_department__or_404(self, department_id: int, employee_id: int) -> None:
        if not await self.repo.exists_in_department(employee_id, department_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работника не существует")
