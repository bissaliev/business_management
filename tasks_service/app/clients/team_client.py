import httpx
from fastapi import HTTPException

from app.config import settings

BASE_TEAM_URL1 = settings.get_team_url()
BASE_TEAM_URL = "http://localhost:8002/teams"


class TeamServiceClient:
    def __init__(self, base_url: str = BASE_TEAM_URL):
        self.base_url = base_url

    async def get_employee(self, team_id: int, user_id: int):
        """Получение работника из Team Service"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/teams/{team_id}/employees/{user_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {}
                # raise HTTPException(status_code=404, detail=f"Работник с {user_id} не существует") from e
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении работника: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail="Сервис Team service не доступен") from e
