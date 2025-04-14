from pydantic import BaseModel


class MessageDelete(BaseModel):
    """Сообщение об удалении"""

    message: str = "Запись удалена"
