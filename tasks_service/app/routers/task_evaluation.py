from fastapi import APIRouter

from app.routers.dependencies import CurrentUser, TaskEvaluationServiceDeps
from app.schemas.task_evaluation import EmployeeEvaluationSummary, TaskEvaluationCreate, TaskEvaluationOut

router = APIRouter()


@router.get(
    "/evaluations/current-employee",
    response_model=EmployeeEvaluationSummary,
    summary="Получение работников матрицы своих оценок",
)
async def get_my_evaluation(
    user: CurrentUser, evaluation_service: TaskEvaluationServiceDeps
) -> EmployeeEvaluationSummary:
    evaluations = await evaluation_service.get_evaluations(user)
    return evaluations


@router.post(
    "/{task_id}/evaluations",
    response_model=TaskEvaluationOut,
    summary="Создание оценки работника за выполненную задачу",
)
async def create_evaluation(
    task_id: int,
    evaluation_data: TaskEvaluationCreate,
    user: CurrentUser,
    evaluation_service: TaskEvaluationServiceDeps,
) -> TaskEvaluationOut:
    evaluation = await evaluation_service.create_evaluation(task_id, user, evaluation_data)
    return evaluation
