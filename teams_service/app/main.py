from fastapi import FastAPI
from sqladmin import Admin

from app.admin.views import TeamAdmin, TeamEmployeeAdmin
from app.database import async_engine
from app.routers.teams import router as team_router

app = FastAPI()
admin = Admin(app, async_engine)

admin.add_view(TeamAdmin)
admin.add_view(TeamEmployeeAdmin)


app.include_router(team_router, prefix="/teams", tags=["teams"])
