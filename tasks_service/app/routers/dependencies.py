from typing import Annotated

from fastapi import Depends, HTTPException, Path, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.rabbitmq.event_publisher import EventPublisher
from app.clients.user_client import UserServiceClient
from app.config import settings
from app.database import get_session
from app.models.tasks import Task
from app.schemas.users import EmployeeRole, User
from app.services.comment_service import CommentService
from app.services.task_evaluation_service import TaskEvaluationService
from app.services.task_service import TaskService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.URL_TOKEN)


def rqm_producer(request: Request) -> EventPublisher:
    return request.app.rqm_producer


EventPublisherDeps = Annotated[EventPublisher, Depends(rqm_producer)]


async def task_service(
    session: Annotated[AsyncSession, Depends(get_session)], rqm_producer: EventPublisherDeps
) -> TaskService:
    """Функция для внедрения в зависимости сервис TaskService"""
    return TaskService(session=session, rmq_producer=rqm_producer)


TaskServiceDeps = Annotated[TaskService, Depends(task_service)]


async def comment_service(session: Annotated[AsyncSession, Depends(get_session)]) -> CommentService:
    """Функция для внедрения в зависимости сервис TaskService"""
    return CommentService(session)


CommentServiceDeps = Annotated[CommentService, Depends(comment_service)]


async def evaluation_service(session: Annotated[AsyncSession, Depends(get_session)]) -> TaskEvaluationService:
    """Функция для внедрения в зависимости сервис TaskService"""
    return TaskEvaluationService(session)


TaskEvaluationServiceDeps = Annotated[TaskEvaluationService, Depends(evaluation_service)]

UserClientDeps = Annotated[UserServiceClient, Depends(lambda: UserServiceClient())]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_client: UserClientDeps) -> User:
    """Проверяет токен через User Service, возвращает данные (id, status, is_active, team_id, team_role)."""
    user_data = await user_client.verify_token(token)
    if not user_data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return User.model_validate(user_data)


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_manager_or_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Разрешает действия только админам руководителям команды (role="менеджер", "админ")"""
    if not user.team_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    if user.role not in [EmployeeRole.MANAGER, EmployeeRole.ADMINISTRATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    return user


ManagerOrAdmin = Annotated[User, Depends(require_manager_or_admin)]


async def current_task(
    task_id: Annotated[int, Path()], session: Annotated[AsyncSession, Depends(get_session)]
) -> Task:
    """Получение запрошенной задачи для дальнейшей проверки"""
    stmt = select(Task).where(Task.id == task_id)
    task = (await session.execute(stmt)).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


CurrentTask = Annotated[Task, Depends(current_task)]


async def require_task_assignee(task: CurrentTask, user: CurrentUser) -> User:
    """
    Разрешает редактирование/комментирование задачи исполнителю (assignee_id), руководителям и администратору.
    """
    if not (user.id == task.creator_id or user.id == task.assignee_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    return user


AssigneePermission = Depends(require_task_assignee)


async def check_team_member_detail(task: CurrentTask, user: Annotated[User, Depends(get_current_user)]) -> None:
    """
    Разрешает действия только участникам команды на основе атрибута задачи team_id.
    """
    if task.team_id != user.team_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")


async def check_team_member_list(
    team_id: Annotated[int, Path()], user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Разрешает действия только участникам команды на основе параметра team_id.
    """
    if user.team_id and team_id != user.team_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не являетесь членом команды")


def check_team_member(detail: bool = True):
    """
    Функция для динамического определения зависимости.
    check_team_member_detail: проверяет доступ на основе запрошенной задачи
    check_team_member_list: проверяет доступ на основе team_id задачи
    """
    if detail:
        return Depends(check_team_member_detail)
    return Depends(check_team_member_list)


TeamMemberPermission = check_team_member


async def require_task_members(task: CurrentTask, user: CurrentUser) -> None:
    """Разрешает действия только участникам задачи."""
    if not (task.creator_id == user.id or task.assignee_id == user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав доступа")


TaskMemberPermission = Depends(require_task_members)
