from pydantic import BaseModel


class MessageDelete(BaseModel):
    message: str = "Запись удалена"
