import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.schemas.users import TeamRoleResponse

BASE_TEAM_URL = settings.get_team_url()


class TeamServiceClient:
    """Клиент для взаимодействия с Team Service"""

    def __init__(self, base_url: str = BASE_TEAM_URL):
        self.base_url = base_url
        self.headers = {"X-API-KEY": settings.TEAM_API_KEY}
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def _request(self, method: str, url: str, **kwargs):
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(method, url, headers=self.headers, **kwargs)
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            if status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ресурс не найден") from e
            if status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверные входные данные") from e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при обращении к Team Service: {status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис команд не доступен"
            ) from e

    async def get_employee_role(self, user_id: int, team_id: int):
        """Получение роли работника из Team Service"""
        url = f"{self.base_url}/teams/{team_id}/employees/{user_id}"
        response = await self._request("GET", url)
        return TeamRoleResponse.model_validate(response.json())

    async def add_employee_to_team(self, employee_id: int, team_code: str):
        """Добавление работника в команду через Team Service"""
        url = f"{self.base_url}/webhook/add_employee/"
        payload = {"team_code": team_code, "employee_id": employee_id}
        response = await self._request("POST", url, json=payload)
        return response.json()
