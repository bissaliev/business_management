from fastapi import FastAPI
from sqladmin import Admin

from app.admin.authentication import authentication_backend
from app.admin.views import TeamAdmin, TeamEmployeeAdmin, TeamNewsAdmin
from app.database import async_engine
from app.routers.employees import router as employee_router
from app.routers.team_news import router as team_news_router
from app.routers.teams import router as team_router
from app.routers.webhook import router as webhook

app = FastAPI(root_path="/teams")
admin = Admin(app, async_engine, authentication_backend=authentication_backend)

admin.add_view(TeamAdmin)
admin.add_view(TeamEmployeeAdmin)
admin.add_view(TeamNewsAdmin)


app.include_router(team_router, prefix="/teams", tags=["teams"])
app.include_router(employee_router, prefix="/teams", tags=["employees"])
app.include_router(team_news_router, prefix="/teams", tags=["team_news"])
app.include_router(webhook, prefix="/webhook", tags=["webhook"])
