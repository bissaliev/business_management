from sqlalchemy import delete, exists, select, update

from app.models import EmployeeStructure
from app.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    model = EmployeeStructure

    async def exists_in_department(self, employee_id: int, department_id: int):
        """Проверка на существование связи работник-департамент"""
        stmt = select(
            exists(self.model).where(self.model.employee_id == employee_id, self.model.department_id == department_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_employees_by_department_id(self, department_id: int) -> list[EmployeeStructure]:
        """Получить список сотрудников по идентификатору департамента"""
        stmt = select(self.model).where(self.model.department_id == department_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_employee(self, employee_id: int):
        """Получить сотрудника"""
        stmt = select(self.model).where(self.model.employee_id == employee_id)
        return (await self.session.scalars(stmt)).first()

    async def update_employee(self, employee_id: int, **data: dict) -> EmployeeStructure:
        stmt = update(self.model).where(self.model.employee_id == employee_id).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_employee(self, employee_id: int) -> bool:
        stmt = delete(self.model).where(self.model.employee_id == employee_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def add_manager(self, department_id: int, manager_id):
        """Получить сотрудника"""
        stmt = (
            update(self.model)
            .where(self.model.department_id == department_id)
            .values(manager_id=manager_id)
            .returning(self.model)
        )
        return (await self.session.scalars(stmt)).all()
