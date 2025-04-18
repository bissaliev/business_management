from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TaskEvaluation(Base):
    """Модель с оценками задачи"""

    __tablename__ = "task_evaluations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    employee_id: Mapped[int]  # Сотрудник, чья задача оценивается
    evaluator_id: Mapped[int]  # Руководитель, выставивший оценку
    timeliness: Mapped[float]  # Оценка за сроки (1–5)
    quality: Mapped[float]  # Оценка за качество (1–5)
    completeness: Mapped[float]  # Оценка за полноту (1–5)
    average_score: Mapped[float]  # Средний балл (вычисляется автоматически)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    task = relationship("Task", back_populates="task_evaluations")

    def __str__(self):
        return f"Средняя оценка {self.average_score}"
