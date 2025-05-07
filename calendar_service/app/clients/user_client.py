import httpx
from fastapi import HTTPException

from app.config import settings
from app.logging_config import logger

BASE_URL = settings.get_user_url()


class UserServiceClient:
    """Клиент для взаимодействия с сервисом User Service"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    async def verify_token(self, token: str) -> dict:
        """Верификация токена"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(
                    f"{self.base_url}/auth/verify", headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при верификации токена: {e}")
            raise HTTPException(status_code=e.response.status_code, detail="Неверный токен или пользователь") from e
        except httpx.ConnectError as e:
            logger.error(f"Сервис User service не доступен: {e}")
            raise HTTPException(status_code=503, detail="Сервис User service не доступен") from e
