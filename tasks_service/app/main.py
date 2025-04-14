from fastapi import FastAPI

from app.routers.tasks import router as task_router

app = FastAPI(root_path="/tasks-service")


app.include_router(task_router, prefix="/tasks", tags=["tasks"])
