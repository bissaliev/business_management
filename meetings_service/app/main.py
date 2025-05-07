from fastapi import FastAPI

from app.routers.meetings import router as meeting_router

app = FastAPI(root_path="/meeting-service")


app.include_router(meeting_router, prefix="/meetings", tags=["meetings"])
