from pydantic import BaseModel


class MessageDelete(BaseModel):
    """Сообщение об удалении записи"""

    message: str = "Запись удалена"
