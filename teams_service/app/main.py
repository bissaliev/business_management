from fastapi import FastAPI
from sqladmin import Admin

from app.admin.views import TeamAdmin, TeamEmployee
from app.database import async_engine
from app.routers.teams import router as team_router

app = FastAPI()
admin = Admin(app, async_engine)

admin.add_view(TeamAdmin)
admin.add_view(TeamEmployee)


app.include_router(team_router, prefix="/teams", tags=["teams"])
