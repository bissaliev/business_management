from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_DB_HOST: str = "localhost"
    AUTH_DB_PORT: int = 5432
    AUTH_USER_DB: str = "postgres"
    AUTH_PASSWORD_DB: str = "postgres"
    AUTH_DB: str = "auth_db"

    TEAM_DB_HOST: str = "teams_db"
    TEAM_DB_PORT: int = 5432

    SECRET_KEY: str = "SECRET_KEY"


settings = Settings()
