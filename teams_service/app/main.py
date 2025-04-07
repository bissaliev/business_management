from fastapi import FastAPI

from app.routers.teams import router as team_router

app = FastAPI()


app.include_router(team_router, prefix="/teams", tags=["teams"])
