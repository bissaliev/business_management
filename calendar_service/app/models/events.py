import enum
from datetime import datetime, timezone

from app.database import Base
from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column


class EventType(enum.Enum):
    """Тип события"""

    MEETING = "meeting"
    TASK = "task"
    PERSONAL = "personal"


class Event(Base):
    """Модель Событий"""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str | None] = mapped_column(String(1000))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))
    source_id: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
