from pydantic import BaseModel


class MessageMeetingDelete(BaseModel):
    """Сообщение об удалении встречи"""

    message: str = "Встреча отменена"


class MessageParticipantAdd(BaseModel):
    """Сообщение об добавлении участника встречи"""

    message: str = "Участник добавлен к встрече"


class MessageParticipantDelete(BaseModel):
    """Сообщение об удалении участника из встречи"""

    message: str = "Участник удален из встречи"
