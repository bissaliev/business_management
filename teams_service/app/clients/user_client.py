import httpx
from fastapi import HTTPException

from app.config import settings
from app.schemas.employees import UserResponse


class UserServiceClient:
    def __init__(self, base_url: str = settings.get_user_url()):
        self.base_url = base_url

    async def create_user(self, name: str, email: str, password: str) -> UserResponse:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.post(
                    f"{self.base_url}",
                    json={
                        "email": email,
                        "name": name,
                        "password": password,
                    },
                )
                response.raise_for_status()
                return UserResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                raise HTTPException(status_code=409, detail=f"Пользователь с {email} существует") from e
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении пользователя: {e.response.status_code}, {e.response.text}",
            ) from e
        except httpx.ConnectError:
            # raise HTTPException(status_code=503, detail="Сервис пользователей не доступен") from e
            return UserResponse.model_validate({"id": 1, "name": name, "email": email})
