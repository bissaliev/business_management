from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.user_client import UserServiceClient
from app.models.teams import Team, TeamEmployee
from app.repositories.team_employee_repo import TeamEmployeeRepository
from app.repositories.team_repo import TeamRepository


class TeamEmployeeService:
    """Сервис для управления работниками в команде"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.team_repo = TeamRepository(session)
        self.repo = TeamEmployeeRepository(session)
        self.user_client = UserServiceClient()

    async def create_employee(self, data: dict) -> TeamEmployee:
        """Регистрация работника"""
        team_code = data.pop("team_code")
        team = await self._get_team_by_team_code(team_code)
        if not team:
            raise HTTPException(status_code=404, detail="Неверный идентификационный код команды")
        new_user = await self.user_client.create_user(**data, team_id=team.id)
        new_employee = await self.repo.add_employee_to_team(team.id, {"employee_id": new_user.id})
        return new_employee

    async def get_team_employees(self, team_id: int) -> TeamEmployee:
        """Получение работников определенной команды"""
        if not await self._exists_team(team_id):
            raise HTTPException(status_code=404, detail="Команды не существует")
        return await self.repo.get_team_employees(team_id)

    async def get_specific_team_employee(self, team_id: int, employee_id: int) -> TeamEmployee:
        """Получение определенного работника команды"""
        employee = await self.repo.get_specific_team_employee(team_id, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Работник не существует в данной команде")
        return employee

    async def update_role(self, team_id: int, employee_id: int, role: dict) -> TeamEmployee:
        """Обновление роли работника"""
        if not await self._exists_employee_team(team_id, employee_id):
            raise HTTPException(status_code=404, detail="Работника не существует в данной команде")
        update_employee = await self.repo.update_role(team_id, employee_id, role)
        return update_employee

    async def delete_employee(self, team_id: int, employee_id: int) -> None:
        """Удаление работника"""
        if not await self._exists_employee_team(team_id, employee_id):
            raise HTTPException(status_code=404, detail="Работника не существует в данной команде")
        await self.user_client.delete_user(employee_id)
        await self.repo.delete_employee(team_id, employee_id)

    async def _exists_employee_team(self, team_id: int, employee_id: int):
        """Проверка на существование работника в команде"""
        return await self.repo.exists_employee_team(team_id, employee_id)

    async def _exists_team(self, team_id: int) -> bool:
        """Проверка на существование команды"""
        return await self.team_repo.exists(team_id)

    async def _get_team_by_team_code(self, team_code: int) -> bool:
        """Проверка на существование команды"""
        return await self.team_repo.get_team_by_team_code(team_code)

    async def _get_team_by_team_code(self, team_code: int) -> Team:
        """Получение команды по team_code"""
        return await self.team_repo.get_team_by_team_code(team_code)
