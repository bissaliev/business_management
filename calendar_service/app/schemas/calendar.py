from datetime import date

from pydantic import BaseModel, Field

from app.schemas.events import EventOut


class YearMonthParams(BaseModel):
    """Параметры для выбора месяц и года"""

    year: int
    month: int = Field(ge=1, le=12)


class CalendarMonthResponse(BaseModel):
    """Отображение событий за месяц"""

    date: date
    events: list[EventOut]

    model_config = {"from_attributes": True}


class CalendarDayResponse(BaseModel):
    """Отображение событий за месяц"""

    events: list[EventOut]

    model_config = {"from_attributes": True}
