from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    TEAM_HOST: str
    TEAM_PORT: str
    ORG_HOST: str
    ORG_PORT: str
    USER_HOST: str
    USER_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: str
    URL_TOKEN: str
    MEETING_API_KEY: str
    LOG_DIR: Path = Path(__file__).parent.parent / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    RABBITMQ_URL: str

    model_config = SettingsConfigDict(env_file=".env")

    def get_db_postgres_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    def get_team_url(self):
        return f"http://{self.TEAM_HOST}:{self.TEAM_PORT}/teams"

    def get_user_url(self):
        return f"http://{self.USER_HOST}:{self.USER_PORT}/users"

    def get_org_url(self):
        return f"http://{self.ORG_HOST}:{self.ORG_PORT}/org"


settings = Setting()
