import httpx
from fastapi import HTTPException, status

from app.config import settings

BASE_URL = settings.get_user_url()


class UserServiceClient:
    """Клиент для запросов на User Service"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    async def _request(self, method: str, url: str, **kwargs) -> dict:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if method == "GET" and "/verify" in url:
                raise HTTPException(status_code=e.response.status_code, detail="Invalid token or user") from e
            return None
        except httpx.ConnectError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис User service не доступен"
            ) from e

    async def get_token(self, username, password) -> str | None:
        """Получение токена аутентификации"""
        response = await self._request(
            "POST", f"{self.base_url}/auth/token", data={"username": username, "password": password}
        )
        return response["access_token"]

    async def verify_token(self, token: str) -> dict:
        """Верификация токена"""
        return await self._request("GET", f"{self.base_url}/auth/verify", headers={"Authorization": f"Bearer {token}"})
