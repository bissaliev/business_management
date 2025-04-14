from fastapi import APIRouter

from app.routers.dependencies import (
    CurrentUser,
    ManagerOrAdmin,
    ManagerOrAssigneePermission,
    TaskServiceDeps,
    TeamMemberPermission,
)
from app.schemas.responses import MessageDelete
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()


@router.get(
    "/teams/{team_id}", dependencies=[TeamMemberPermission(detail=False)], summary="Получить все задачи команды"
)
async def get_teams_tasks(team_id: int, task_service: TaskServiceDeps):
    return await task_service.get_tasks(team_id)


@router.get("/assigned_tasks", summary="Получить назначенные задачи")
async def get_assigned_tasks(user: CurrentUser, task_service: TaskServiceDeps):
    return await task_service.get_assigned_tasks(user)


@router.post("/", response_model=TaskResponse, summary="Создание задачи")
async def create_task(task_data: TaskCreate, user: ManagerOrAdmin, task_service: TaskServiceDeps):
    return await task_service.create_task(user, task_data.model_dump(exclude_unset=True))


@router.get("/{task_id}", summary="Получение задачи", dependencies=[TeamMemberPermission(detail=True)])
async def get_task(task_id: int, task_service: TaskServiceDeps) -> TaskResponse:
    return await task_service.get_task(task_id)


@router.patch("/{task_id}", dependencies=[ManagerOrAssigneePermission], summary="Обновление задачи")
async def update_task(task_id: int, task_data: TaskUpdate, task_service: TaskServiceDeps) -> TaskResponse:
    return await task_service.update_task(task_id, task_data.model_dump(exclude_unset=True))


@router.delete("/{task_id}", dependencies=[ManagerOrAssigneePermission], summary="Удаление выполненной задачи")
async def delete_task(task_id: int, task_service: TaskServiceDeps) -> MessageDelete:
    await task_service.delete_task(task_id)
    return MessageDelete()
