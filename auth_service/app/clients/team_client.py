import httpx
from fastapi import HTTPException

from app.config import settings
from app.schemas.users import TeamRoleResponse

BASE_TEAM_URL = settings.get_team_url()


class TeamServiceClient:
    def __init__(self, base_url: str = BASE_TEAM_URL):
        self.base_url = base_url

    async def get_employee_role(self, user_id: int, team_id: int):
        """Получение работника из Team Service"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/teams/{team_id}/employees/{user_id}")
                response.raise_for_status()
                return TeamRoleResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Работник с {user_id} не существует") from e
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении работника: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail="Сервис команд не доступен") from e
