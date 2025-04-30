import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.logging_config import logger

BASE_TEAM_URL = settings.get_team_url()


class TeamServiceClient:
    """Клиент для запросов на Team Service"""

    def __init__(self, base_url: str = BASE_TEAM_URL):
        self.base_url = base_url
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def _request(self, method: str, endpoint: str, *, json=None, params=None) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    json=json,
                    params=params,
                )
                response.raise_for_status()
                return response.status_code == status.HTTP_200_OK
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при запросе {e.request.url}: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e)) from e
        except httpx.ConnectError as e:
            logger.error(f"Сервис Team service не доступен: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис Team service не доступен"
            ) from e

    async def get_employee(self, team_id: int, user_id: int):
        """Получение работника команды из Team Service"""
        return await self._request("GET", f"/teams/{team_id}/employees/{user_id}")

    async def get_team_members(self, team_id: int) -> list[dict]:
        """Получение участников команды из Team Service"""
        return await self._request("GET", f"/teams/{team_id}/employees")
