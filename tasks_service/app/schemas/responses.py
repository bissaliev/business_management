from pydantic import BaseModel


class MessageDelete(BaseModel):
    message: str = "Задача удалена"
