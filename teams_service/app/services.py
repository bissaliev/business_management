import httpx
from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.teams import Team, TeamEmployee


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team_by_code(self, team_code: str):
        stmt = select(Team).where(Team.team_code == team_code)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_team_by_id(self, team_id: int):
        stmt = select(Team).where(Team.team_id == team_id)
        result = await self.session.scalars(stmt)
        return result.first()

    async def create_team(self, team_data: dict):
        result = await self.session.scalars(insert(Team).values(**team_data).returning(Team))
        return result.first()

    async def get_employee(self, user_id: int):
        async with httpx.AsyncClient() as client:
            url = f"{settings.USER_HOST}/{settings.USER_PORT}/users/{user_id}"
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Пользователь с таким user_id={user_id} не существует")
        return response.json()

    async def employee_exists(self, employee_id: int):
        async with httpx.AsyncClient() as client:
            url = f"{settings.USER_HOST}/{settings.USER_PORT}/users/{employee_id}"
            response = await client.get(url)
            if response.status_code == 200:
                return True
        return False

    async def add_employee(self, team_id: int, data: dict):
        """Добавление сотрудника в команду"""
        employee_id = data["employee_id"]
        employee_exists = await self.get_employee(employee_id)
        if not employee_exists:
            raise HTTPException(status_code=404, detail=f"Пользователь с таким user_id={employee_id} не существует")
        team = await self.get_team_by_id(team_id)
        stmt = insert(TeamEmployee).values(team_id=team.id, **data)
        await self.session.execute(stmt)
