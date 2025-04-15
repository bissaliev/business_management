from fastapi import FastAPI

from app.routers.comments import router as comment_router
from app.routers.task_evaluation import router as task_evaluation_router
from app.routers.tasks import router as task_router

app = FastAPI(root_path="/tasks-service")


app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(comment_router, prefix="/tasks", tags=["comments"])
app.include_router(task_evaluation_router, prefix="/tasks", tags=["task evaluation"])
