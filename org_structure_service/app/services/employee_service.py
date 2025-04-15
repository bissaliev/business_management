# import httpx
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models import EmployeeRole, EmployeeStructure
from app.repositories.department_repo import DepartmentRepository
from app.repositories.employee_repo import EmployeeRepository


class EmployeeService:
    """Сервис Организационной структуры команды"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeRepository(session)
        self.department_repo = DepartmentRepository(session)
        self.team_client = TeamServiceClient()

    async def exists(self, id: int) -> bool:
        """Проверка на существование работника в организационной структуре"""
        return await self.repo.exists(id)

    async def exists_department(self, department_id: int) -> bool:
        """Проверка на существование департамента"""
        return await self.department_repo.exists(department_id)

    async def get_department(self, department_id: int) -> bool:
        """Проверка на существование департамента"""
        return await self.department_repo.get(department_id)

    async def get_employee_in_team_service(self, team_id: int, user_id: int) -> bool:
        """Проверка на существование работника в team_service"""
        return await self.team_client.get_employee(team_id, user_id)

    async def exists_in_department(self, employee_id: int, department_id: int) -> bool:
        """Проверка на существование связи работника и департамента"""
        return await self.repo.exists_in_department(employee_id, department_id)

    async def add_employee(self, employee_data: dict) -> EmployeeStructure:
        """Добавление работника в организационную структуру"""
        try:
            if "department_id" in employee_data:
                department = await self.get_department(employee_data["department_id"])
                if not department:
                    raise HTTPException(status_code=404, detail="Департамент не существует")

                if await self.exists_in_department(employee_data["employee_id"], employee_data["department_id"]):
                    raise HTTPException(status_code=400, detail="Работник уже зарегистрирован в данном департаменте")

                employee = await self.get_employee_in_team_service(department.team_id, employee_data["employee_id"])
                if not employee:
                    raise HTTPException(status_code=404, detail="Данного работника не существует в команде")
                employee = await self.repo.add(**employee_data)
                return employee
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def update_employee(self, employee_id: int, employee_data: dict) -> EmployeeStructure:
        """Обновление данных"""
        try:
            if not await self.exists(employee_id):
                raise HTTPException(status_code=404, detail="Работника не существует в организационной структуре")

            if "department_id" in employee_data:
                department = await self.get_department(employee_data["department_id"])
                if not department:
                    raise HTTPException(status_code=404, detail="Департамент не существует")

            if "manager_id" in employee_data:
                manager = await self.get_employee_in_team_service(department.team_id, employee_data["manager_id"])
                if not manager:
                    raise HTTPException(status_code=404, detail="Данного работника не существует в команде")
                if manager.role != EmployeeRole.MANAGER:
                    raise HTTPException(status_code=404, detail="Данный работник не является менеджером")
                return await self.repo.update(id, **employee_data)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def get_employees(self, department_id: int) -> list[EmployeeStructure]:
        """Получить список всех сотрудников"""
        if department_id:
            return await self.repo.get_employees_by_department_id(department_id)
        return await self.repo.get_all()

    async def get_employee(self, employee_id: int) -> EmployeeStructure:
        """Получить сотрудника"""
        employee = await self.repo.get_employee(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Работника не существует в организационной структуре")
        return employee

    async def get_department_members(self, employee_id: int) -> list[EmployeeStructure]:
        """Получить всех коллег департамента сотрудника"""
        employee = await self.repo.get_employee(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Работника не существует")
        members = await self.repo.get_employees_by_department_id(employee.department_id)
        return members

    async def add_manager(self, department_id: int, manager_id: int) -> None:
        """Назначение руководителя сотрудникам"""
        try:
            department = await self.get_department(department_id)
            if not department:
                raise HTTPException(status_code=404, detail="Департамент не существует")
            employee = await self.get_employee_in_team_service(department.team_id, manager_id)
            if not employee:
                raise HTTPException(status_code=404, detail="Данного работника не существует в команде")
            if employee.role != EmployeeRole.MANAGER:
                raise HTTPException(status_code=404, detail="Данный работник не является менеджером")
            await self.repo.add_manager(department_id, manager_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def delete_employee(self, employee_id: int):
        """Удаление работника"""
        if not await self.exists(employee_id):
            raise HTTPException(status_code=404, detail="Работника не существует в организационной структуре")
        try:
            return await self.repo.delete_employee(employee_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
