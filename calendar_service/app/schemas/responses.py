from pydantic import BaseModel


class MessageEventDelete(BaseModel):
    """Сообщение об удалении события"""

    message: str = "Событие удалено"
