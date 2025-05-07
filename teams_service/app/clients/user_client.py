import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.logging_config import logger
from app.schemas.employees import UserResponse

BASE_URL_USER_SERVICE = settings.get_user_url()


class UserServiceClient:
    """Клиент для запросов к user service"""

    def __init__(self, base_url: str = BASE_URL_USER_SERVICE):
        self.base_url = base_url
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def _request(self, method: str, endpoint: str, *, json=None) -> dict:
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(method, url, json=json)
                response.raise_for_status()
                if response.content:
                    return response.json()
                return {}
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при запросе {e.request.url}: {e}")
            status_code = e.response.status_code
            detail = e.response.text

            if status_code == status.HTTP_409_CONFLICT:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует") from e
            if status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден") from e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка user service: {status_code}, {detail}",
            ) from e

        except httpx.ConnectError as e:
            logger.error(f"Сервис User service не доступен: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="User service недоступен"
            ) from e

    async def create_user(self, name: str, email: str, password: str, team_id: int) -> UserResponse:
        """Создание пользователя в User Service"""
        data = {"email": email, "name": name, "password": password, "team_id": team_id}
        json_data = await self._request("POST", "/auth/register", json=data)
        return UserResponse.model_validate(json_data)

    async def delete_user(self, user_id: int) -> None:
        """Удаление пользователя в User Service"""
        await self._request("DELETE", f"/users/{user_id}")


class AuthClient:
    """Клиент для запросов на User Service для аутентификации"""

    def __init__(self, base_url: str = BASE_URL_USER_SERVICE):
        self.base_url = base_url

    async def _request(self, method: str, url: str, **kwargs) -> dict | None:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при запросе {e.request.url}: {e}")
            if method == "GET" and "/verify" in url:
                raise HTTPException(status_code=e.response.status_code, detail="Invalid token or user") from e
            return None
        except httpx.ConnectError as e:
            logger.error(f"Сервис User service не доступен: {e}")
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
