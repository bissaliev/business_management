from sqlalchemy import delete, exists, select, update

from app.models import EmployeeStructure
from app.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    """Репозиторий для управления работниками"""

    model: type[EmployeeStructure] = EmployeeStructure

    async def exists_in_department(self, employee_id: int, department_id: int) -> bool:
        """Проверка на существование связи работник-департамент"""
        stmt = select(exists().where(self.model.employee_id == employee_id, self.model.department_id == department_id))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def get_employees_by_department_id(self, department_id: int) -> list[EmployeeStructure]:
        """Получить список сотрудников по идентификатору департамента"""
        stmt = select(self.model).where(self.model.department_id == department_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_employee(self, department_id: int, employee_id: int) -> EmployeeStructure:
        """Получить сотрудника"""
        stmt = select(self.model).where(
            self.model.department_id == department_id, self.model.employee_id == employee_id
        )
        return (await self.session.scalars(stmt)).first()

    async def get_employee_by_employee_id(self, employee_id: int) -> EmployeeStructure:
        """Получение работника по employee_id"""
        stmt = select(self.model).where(self.model.employee_id == employee_id)
        return (await self.session.scalars(stmt)).first()

    async def update_employee(self, employee_id: int, **data: dict) -> EmployeeStructure:
        """Обновление работника по employee_id"""
        stmt = update(self.model).where(self.model.employee_id == employee_id).values(**data).returning(self.model)
        result = await self.session.scalars(stmt)
        return result.first()

    async def delete_employee(self, employee_id: int, department_id: int) -> bool:
        """Удаление работника по employee_id"""
        stmt = delete(self.model).where(
            self.model.employee_id == employee_id, self.model.department_id == department_id
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def add_manager(self, department_id: int, manager_id) -> None:
        """Назначить менеджера работникам из одного департамента"""
        stmt = (
            update(self.model)
            .where(self.model.department_id == department_id)
            .values(manager_id=manager_id)
            .returning(self.model)
        )
        await self.session.scalars(stmt)
