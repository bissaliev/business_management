import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class TaskStatus(str, enum.Enum):
    """Статус задачи"""

    OPEN = "открыто"
    IN_PROGRESS = "в работе"
    COMPLETED = "выполнено"


class Task(Base):
    """Модель задач"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus, native_enum=False), default=TaskStatus.OPEN)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    creator_id: Mapped[int]  # Создатель (руководитель)
    assignee_id: Mapped[int]  # Исполнитель (подчинённый)
    team_id: Mapped[int]  # Команда

    task_evaluations = relationship("TaskEvaluation", back_populates="task")

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, status={self.status})"

    def __str__(self):
        return self.title
