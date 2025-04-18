from fastapi import FastAPI
from sqladmin import Admin

from app.admin.authentication import authentication_backend
from app.admin.views import TaskAdmin, TaskEvaluationAdmin
from app.database import SessionLocal
from app.routers.comments import router as comment_router
from app.routers.task_evaluation import router as task_evaluation_router
from app.routers.tasks import router as task_router

app = FastAPI(root_path="/tasks-service")


app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(comment_router, prefix="/tasks", tags=["comments"])
app.include_router(task_evaluation_router, prefix="/tasks", tags=["task evaluation"])

admin = Admin(app, session_maker=SessionLocal, authentication_backend=authentication_backend)
admin.add_view(TaskAdmin)
admin.add_view(TaskEvaluationAdmin)
