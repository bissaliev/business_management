import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.schemas.team_response import TeamEmployeeResponse, TeamResponse

TEAM_BASE_URL: str = settings.get_team_service__url()


class TeamServiceClient:
    """Клиент для взаимодействия с Team Service"""

    def __init__(self, base_url: str = TEAM_BASE_URL):
        self.base_url = base_url
        self._timeout = httpx.Timeout(10.0, connect=5.0)

    async def _get(self, url: str) -> dict | None:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(f"{self.base_url}{url}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ошибка при запросе к Team Service: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Сервис Team Service недоступен: {e.__class__.__name__}",
            ) from e

    async def get_team(self, team_id: int) -> TeamResponse | None:
        """Получение команды по ID"""
        data = await self._get(f"/teams/{team_id}")
        return TeamResponse.model_validate(data) if data else None

    async def get_employee(self, team_id: int, employee_id: int) -> TeamEmployeeResponse | None:
        """Получение сотрудника команды"""
        data = await self._get(f"/teams/{team_id}/employees/{employee_id}")
        return TeamEmployeeResponse.model_validate(data) if data else None
