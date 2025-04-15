import httpx
from fastapi import HTTPException

from app.config import settings

BASE_ORG_URL = settings.get_org_url()
# TODO: Убрать заглушку
BASE_ORG_URL = "http://localhost:8003/org"


class OrgServiceClient:
    """Клиент для запросов на Org Structure Service"""

    def __init__(self, base_url: str = BASE_ORG_URL):
        self.base_url = base_url

    async def get_membership(self, employee_id: int) -> dict:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/employees/{employee_id}/department_members")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Работник с {employee_id} не существует") from e
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении работника: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail="Сервис Team service не доступен") from e
