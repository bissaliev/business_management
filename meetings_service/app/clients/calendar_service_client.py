import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.logging_config import logger

BASE_URL_CALENDAR = settings.get_calendar_url()


class CalendarServiceClient:
    """Клиент для управление событиями в сервисе Calendar Service"""

    def __init__(self, base_url: str = BASE_URL_CALENDAR):
        self.base_url = base_url
        self.headers = {"X-API-KEY": settings.API_KEY_CALENDAR}
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def _request(self, method: str, endpoint: str, *, json=None, params=None) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    json=json,
                    params=params,
                )
                response.raise_for_status()
                return response.status_code == status.HTTP_200_OK
        except httpx.HTTPStatusError as e:
            # Специальная обработка 404 только для verify
            if method == "GET" and response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            logger.error(f"Ошибка при запросе {e.request.url}: {e}")
            raise HTTPException(status_code=e.response.status_code, detail="Неизвестная ошибка") from e
        except httpx.ConnectError as e:
            logger.error(f"Сервис Calendar service не доступен: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис Calendar service не доступен"
            ) from e

    async def send_meeting_webhook(self, meeting: dict) -> bool:
        """Создание события о встрече"""
        return await self._request("POST", "/webhooks/new-event", json=meeting)

    async def delete_meeting_webhook(self, meeting: dict) -> bool:
        """Удаление события о встрече"""
        return await self._request("DELETE", "/webhooks/remove-event", params=meeting)

    async def has_events_in_period(self, meeting: dict) -> bool:
        """Проверка назначенных событий у пользователя в заданный период"""
        return await self._request("GET", "/webhooks/verify-event", params=meeting)
