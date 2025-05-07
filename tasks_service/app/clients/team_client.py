import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.logging_config import logger

BASE_TEAM_URL = settings.get_team_url()


class TeamServiceClient:
    """Клиент для взаимодействия с сервисом Team Service"""

    def __init__(self, base_url: str = BASE_TEAM_URL):
        self.base_url = base_url

    async def get_employee(self, team_id: int, user_id: int) -> dict:
        """Получение работника из Team Service"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/teams/{team_id}/employees/{user_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.info(f"Ошибка при запросе на {e.request.url}: {e}")
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Работник с {user_id} не существует"
                ) from e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при получении работника: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            logger.info("Сервис Team service не доступен")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис Team service не доступен"
            ) from e
