from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    TEAM_HOST: str
    TEAM_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")

    def get_db_postgres_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    def get_team_url(self):
        return f"http://{self.TEAM_HOST}:{self.TEAM_PORT}/teams"


settings = Setting()
