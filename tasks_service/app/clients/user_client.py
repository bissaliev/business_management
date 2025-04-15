# task_service/clients/user_service_client.py
import httpx
from fastapi import HTTPException

from app.config import settings

BASE_URL = settings.get_user_url()


class UserServiceClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    async def verify_token(self, token: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                response = await client.get(
                    f"{self.base_url}/auth/verify", headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Invalid token or user") from e
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail="Сервис User service не доступен") from e
