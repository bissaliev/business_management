from fastapi import APIRouter, status

from app.routers.dependencies import CommentServiceDeps, CurrentUser, TaskMemberPermission
from app.schemas.comments import CommentCreate, CommentResponse

router = APIRouter()


@router.post(
    "/{task_id}/comments",
    response_model=CommentResponse,
    dependencies=[TaskMemberPermission],
    summary="Добавление комментария",
)
async def add_comment(
    task_id: int, comment_data: CommentCreate, user: CurrentUser, comment_service: CommentServiceDeps
) -> CommentResponse:
    return await comment_service.create_comment(task_id, user, comment_data)


@router.get(
    "/{task_id}/comments",
    response_model=list[CommentResponse],
    dependencies=[TaskMemberPermission],
    summary="Получение комментариев задачи",
)
async def get_comments(task_id: int, comment_service: CommentServiceDeps) -> list[CommentResponse]:
    return await comment_service.get_comments_by_task_id(task_id)


@router.patch(
    "/{task_id}/comments/{comment_id}",
    response_model=CommentResponse,
    dependencies=[TaskMemberPermission],
    summary="Обновление комментария",
)
async def update_comment(
    task_id: int, comment_id: int, comment_data: CommentCreate, user: CurrentUser, comment_service: CommentServiceDeps
) -> CommentResponse:
    return await comment_service.update_comment(task_id, comment_id, user, comment_data)


@router.delete(
    "/{task_id}/comments{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[TaskMemberPermission],
    summary="Удаление комментария",
)
async def delete_comment(
    task_id: int, comment_id: int, user: CurrentUser, comment_service: CommentServiceDeps
) -> None:
    await comment_service.delete_comment(task_id, user, comment_id)
