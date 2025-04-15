from datetime import datetime

from pydantic import BaseModel, Field


class TaskEvaluationCreate(BaseModel):
    """Модель для создания оценки задачи"""

    timeliness: float = Field(ge=1, le=5)
    quality: float = Field(ge=1, le=5)
    completeness: float = Field(ge=1, le=5)


class TaskEvaluationOut(BaseModel):
    """Модель ответа оценок"""

    id: int
    task_id: int
    employee_id: int
    evaluator_id: int
    timeliness: float
    quality: float
    completeness: float
    average_score: float
    created_at: datetime

    model_config = {"from_attributes": True}


class EmployeeEvaluationSummary(BaseModel):
    """Модель для предоставления матрицы оценок"""

    employee_id: int
    average_quarterly_score: float
    average_department_score: float
    evaluations: list[TaskEvaluationOut]
