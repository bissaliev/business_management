from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.clients.user_client import AuthClient
from app.config import settings
from app.logging_config import logger
from app.schemas.users import Status


class AdminAuth(AuthenticationBackend):
    """Аутентификация в админ панели"""

    user_client = AuthClient()

    async def login(self, request: Request) -> bool:
        """Для входа выполняем запрос на User Service и сохраняем токен в сессиях"""
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        token = await self.user_client.get_token(username, password)

        if token:
            request.session.update({"token": token})
            logger.info(f"Администратор {username} вошел в систему")
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Очищаем сессии"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Для аутентификации выполняем запрос на User Service"""
        token = request.session.get("token")
        if not token:
            return False

        user = await self.user_client.verify_token(token)
        return user and user["status"] == Status.ADMIN.value


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
