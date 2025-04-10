from sqlalchemy import exists, select

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

    async def get_department_employees(self, department_id: int) -> list[EmployeeStructure]:
        """Получить список сотрудников по идентификатору департамента"""
        stmt = select(self.model).where(self.model.department_id == department_id)
        result = await self.session.scalars(stmt)
        return result.all()
