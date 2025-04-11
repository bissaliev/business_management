# import httpx
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EmployeeManagers
from app.repositories.employee_manager_repo import EmployeeManagerRepository
from app.repositories.employee_repo import EmployeeRepository


class EmployeeManagerService:
    """"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeManagerRepository(session)
        self.employee_repo = EmployeeRepository(session)

    # TODO: Определить логику проверки пользователя в user_service
    # TODO: Определить логику проверки роли пользователя
    async def exists_user_in_user_service(self, user_id: int) -> bool:
        """Проверка на существование пользователя в БД user_service"""
        return bool(user_id)

    async def exists_employee_structure(self, employee_structure_id: int) -> bool:
        return await self.employee_repo.exists(employee_structure_id)

    async def add_manager(self, data: dict) -> EmployeeManagers:
        """Добавление дополнительного руководителя"""
        if not await self.exists_user_in_user_service(data["manager_id"]):
            raise HTTPException(status_code=404, detail="Данного менеджера не существует в БД")

        if not await self.exists_employee_structure(data["employee_structure_id"]):
            raise HTTPException(status_code=404, detail="Данной орг. структуры не существует в БД")
        try:
            emp_man = await self.repo.add(data)
            return emp_man
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="") from e
