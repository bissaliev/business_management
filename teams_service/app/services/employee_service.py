from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.user_client import UserServiceClient
from app.logging_config import logger
from app.models.teams import TeamEmployee
from app.repositories.team_employee_repo import TeamEmployeeRepository
from app.repositories.team_repo import TeamRepository
from app.schemas.employees import EmployeeCreate, EmployeeUpdateRole


class TeamEmployeeService:
    """Сервис для управления работниками в команде"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.team_repo = TeamRepository(session)
        self.repo = TeamEmployeeRepository(session)
        self.user_client = UserServiceClient()

    async def create_employee(self, team_id: int, data: EmployeeCreate) -> TeamEmployee:
        """Регистрация работника"""
        await self._exists_team(team_id)
        new_user = await self.user_client.create_user(**data.model_dump(exclude=["role"]), team_id=team_id)
        new_employee = await self.repo.create(team_id=team_id, employee_id=new_user.id, role=data.role)
        await self.session.commit()
        logger.info(f"Зарегистрирован работник {new_employee.employee_id} в команде {team_id}")
        return new_employee

    async def get_team_employees(self, team_id: int) -> TeamEmployee:
        """Получение работников определенной команды"""
        await self._exists_team(team_id)
        return await self.repo.get_team_employees(team_id)

    async def get_specific_team_employee(self, team_id: int, employee_id: int) -> TeamEmployee:
        """Получение определенного работника команды"""
        employee = await self.repo.get_specific_team_employee(team_id, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Работник не существует в данной команде"
            )
        return employee

    async def update_role(self, team_id: int, employee_id: int, role: EmployeeUpdateRole) -> TeamEmployee:
        """Обновление роли работника"""
        await self._exists_employee_team(team_id, employee_id)
        update_employee = await self.repo.update_role(team_id, employee_id, role.model_dump())
        await self.session.commit()
        logger.info(f"Обновлена роль работника {employee_id} в команде {team_id}")
        return update_employee

    async def delete_employee(self, team_id: int, employee_id: int) -> None:
        """Удаление работника"""
        await self._exists_employee_team(team_id, employee_id)
        await self.user_client.delete_user(employee_id)
        await self.repo.delete_employee(team_id, employee_id)
        await self.session.commit()
        logger.info(f"Удален работник {employee_id} из команды {team_id}")

    async def _exists_employee_team(self, team_id: int, employee_id: int) -> None:
        """Проверка на существование работника в команде"""
        if not await self.repo.exists_employee_team(team_id, employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Работника не существует в данной команде"
            )

    async def _exists_team(self, team_id: int) -> None:
        """Проверка на существование команды"""
        if not await self.team_repo.exists(team_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команды не существует")
