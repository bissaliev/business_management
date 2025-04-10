# import httpx
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EmployeeStructure
from app.repositories.department_repo import DepartmentRepository
from app.repositories.employee_repo import EmployeeRepository


class EmployeeService:
    """Сервис Организационной структуры команды"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeRepository(session)
        self.department_repo = DepartmentRepository(session)

    async def exists_department(self, department_id: int):
        """Проверка на существование департамента"""
        return await self.department_repo.exists(department_id)

    # TODO: Определить логику проверки пользователя в user_service
    async def exists_user_in_user_service(self, user_id: int) -> EmployeeStructure:
        """Проверка на существование пользователя в БД user_service"""
        return bool(user_id)

    async def exists_in_department(self, employee_id, department_id):
        """Проверка на существование связи работника и департамента"""
        return await self.repo.exists_in_department(employee_id, department_id)

    async def add_employee(self, employee_data: dict) -> EmployeeStructure:
        """Добавление работника в организационную структуру"""
        if not await self.exists_user_in_user_service(employee_data["employee_id"]):
            raise HTTPException(status_code=404, detail="Данного работника не существует в БД")
        if "department_id" in employee_data:
            if not await self.exists_department(employee_data["department_id"]):
                raise HTTPException(status_code=404, detail="Департамент не существует")

            if await self.exists_in_department(employee_data["employee_id"], employee_data["department_id"]):
                raise HTTPException(status_code=400, detail="Работник уже зарегистрирован в данном департаменте")

        try:
            employee = await self.repo.add(employee_data)
            return employee
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def get_employees(self) -> list[EmployeeStructure]:
        """Получить список всех сотрудников"""
        return await self.repo.get_all()

    async def get_department_employees(self, department_id: int) -> list[EmployeeStructure]:
        """Получить список сотрудников по идентификатору департамента"""
        return await self.repo.get_department_employees(department_id)
