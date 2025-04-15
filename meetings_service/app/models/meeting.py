from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    team_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Команда
    creator_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Создатель
    participants: Mapped[list[int]] = mapped_column(JSONB, nullable=False)  # Список employee_id
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(ZoneInfo("UTC")), type_=DateTime(timezone=True)
    )
