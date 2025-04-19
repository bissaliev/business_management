from sqladmin import ModelView

from app.models.teams import Team, TeamEmployee, TeamNews


class TeamAdmin(ModelView, model=Team):
    column_list = ["id", "name", "team_code"]
    form_excluded_columns = ["team_code"]


class TeamNewsAdmin(ModelView, model=TeamNews):
    column_list = ["id", "title", "team_id", "created_at"]
    form_excluded_columns = ["created_at"]


class TeamEmployeeAdmin(ModelView, model=TeamEmployee):
    column_list = ["id", "employee_id", "team_id", "role"]
