import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.logging_config import logger

BASE_ORG_URL = settings.get_org_url()


class OrgServiceClient:
    """Клиент для запросов на Org Structure Service"""

    def __init__(self, base_url: str = BASE_ORG_URL):
        self.base_url = base_url

    async def get_membership(self, employee_id: int) -> dict:
        """Получение всех коллег работника по департаменту"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/employees/{employee_id}/department_members")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при запросе {e.request.url}: {e}")
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Работник с {employee_id} не существует"
                ) from e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при получении работника: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            logger.error(f"Сервис Calendar service не доступен: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис Org Structure service не доступен"
            ) from e
