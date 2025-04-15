import httpx
from fastapi import HTTPException
from pydantic import UUID4, BaseModel

from app.config import settings
from app.schemas.employees import TeamEmployeeResponse


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str
    team_code: UUID4


TEAM_BASE_URL: str = settings.get_team_service__url()
# TEAM_BASE_URL = "http://localhost:8002/teams"


class TeamServiceClient:
    """Клиент для взаимодействия с Team Service"""

    def __init__(self, base_url: str = TEAM_BASE_URL):
        self.base_url = base_url

    async def get_team(self, team_id: int) -> TeamResponse:
        """Получение команды"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/{team_id}")
                response.raise_for_status()
                return TeamResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise HTTPException(
                status_code=502,
                detail=f"Ошибка при получении команды: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Сервис команд недоступен: {e.__class__.__name__}") from e

    async def get_employee(self, team_id: int, employee_id: int) -> TeamEmployeeResponse:
        """Получение работника"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/teams/{team_id}/employees/{employee_id}")
                response.raise_for_status()
                return TeamEmployeeResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise HTTPException(
                status_code=502,
                detail=f"Ошибка при получении команды: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Сервис команд недоступен: {e.__class__.__name__}") from e
