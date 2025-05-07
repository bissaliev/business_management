from fastapi import APIRouter, status

from app.routers.dependencies import (
    AssigneePermission,
    CurrentUser,
    ManagerOrAdmin,
    TaskServiceDeps,
    TeamMemberPermission,
)
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()


@router.get(
    "/teams/{team_id}",
    response_model=list[TaskResponse],
    dependencies=[TeamMemberPermission(detail=False)],
    summary="Получить все задачи команды",
)
async def get_teams_tasks(team_id: int, task_service: TaskServiceDeps) -> list[TaskResponse]:
    return await task_service.get_tasks(team_id)


@router.get("/assigned_tasks", response_model=list[TaskResponse], summary="Получить назначенные задачи")
async def get_assigned_tasks(user: CurrentUser, task_service: TaskServiceDeps) -> list[TaskResponse]:
    return await task_service.get_assigned_tasks(user)


@router.post("/", response_model=TaskResponse, summary="Создание задачи")
async def create_task(task_data: TaskCreate, user: ManagerOrAdmin, task_service: TaskServiceDeps) -> TaskResponse:
    return await task_service.create_task(user, task_data)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получение задачи",
    dependencies=[TeamMemberPermission(detail=True)],
)
async def get_task(task_id: int, task_service: TaskServiceDeps) -> TaskResponse:
    return await task_service.get_task(task_id)


@router.patch(
    "/{task_id}", response_model=TaskResponse, dependencies=[AssigneePermission], summary="Обновление задачи"
)
async def update_task(task_id: int, task_data: TaskUpdate, task_service: TaskServiceDeps) -> TaskResponse:
    return await task_service.update_task(task_id, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[AssigneePermission],
    summary="Удаление выполненной задачи",
)
async def delete_task(task_id: int, user: ManagerOrAdmin, task_service: TaskServiceDeps) -> None:
    await task_service.delete_task(user, task_id)
