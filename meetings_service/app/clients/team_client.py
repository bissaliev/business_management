import httpx
from fastapi import HTTPException

from app.config import settings

BASE_TEAM_URL = settings.get_team_url()


class TeamServiceClient:
    """Клиент для запросов на Team Service"""

    def __init__(self, base_url: str = BASE_TEAM_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_employee(self, team_id: int, user_id: int):
        """Получение работника команды из Team Service"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/teams/{team_id}/employees/{user_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Работник с {user_id} не существует") from e
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении работника: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail="Сервис Team service не доступен") from e

    async def get_team_members(self, team_id: int) -> list[dict]:
        """Получение участников команды из Team Service"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/teams/{team_id}/employees")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Команда с {team_id=} не найдена") from e
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail="Сервис Team service не доступен") from e
