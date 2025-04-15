import httpx
from fastapi import HTTPException

from app.config import settings
from app.schemas.employees import UserResponse


class UserServiceClient:
    """ "Клиент для запросов на User Service"""

    def __init__(self, base_url: str = settings.get_user_url()):
        self.base_url = base_url

    async def get_user(self, employee_id: int) -> UserResponse:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(f"{self.base_url}/users/{employee_id}")
                response.raise_for_status()
                return UserResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise HTTPException(
                status_code=502,
                detail=f"Ошибка при получении пользователя: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Сервис пользователей недоступен: {e.__class__.__name__}"
            ) from e
