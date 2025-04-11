import uuid

import httpx
from fastapi import HTTPException
from pydantic import UUID4, BaseModel

from app.config import settings


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str
    team_code: UUID4


class TeamServiceClient:
    def __init__(self, base_url: str = settings.get_team_service__url()):
        self.base_url = base_url

    async def get_team(self, team_id: int) -> TeamResponse:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/{team_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise HTTPException(
                status_code=502,
                detail=f"Ошибка при получении команды: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.RequestError:
            # raise HTTPException(
            #     status_code=503, detail=f"Сервис команд недоступен: {e.__class__.__name__}"
            # ) from e
            # TODO: Поставлена заглушка при получении команд
            team_data = {
                "id": team_id,
                "name": f"Team {team_id}",
                "description": f"Team {team_id}",
                "team_code": uuid.uuid4(),
            }
            return TeamResponse.model_validate(team_data)
