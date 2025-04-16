from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Participant(BaseModel):
    """Участник встречи"""

    participant_id: int


class MeetingCreate(BaseModel):
    """Создание встречи"""

    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    team_id: int


class MeetingUpdate(BaseModel):
    """Обновление встречи"""

    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]


class MeetingOut(BaseModel):
    """Модель ответ при создание и редактирование"""

    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    team_id: int
    creator_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MeetingParticipantOut(BaseModel):
    """Модель ответ при получение встреч"""

    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    team_id: int
    creator_id: int
    participants: list[Participant] = []
    created_at: datetime

    model_config = {"from_attributes": True}
