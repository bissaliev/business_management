from sqladmin import ModelView

from app.models.teams import Team, TeamEmployee


class TeamAdmin(ModelView, model=Team):
    column_list = ["id", "name", "team_code"]


class TeamEmployeeAdmin(ModelView, model=TeamEmployee):
    column_list = ["id", "user_id", "team_id", "role"]
