from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    SECRET_KEY: str
    USER_HOST: str
    USER_PORT: str
    USER_API_KEY: str
    URL_TOKEN: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: str

    model_config = SettingsConfigDict(env_file=".env")

    def get_db_postgres_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    def get_user_url(self):
        return f"http://{self.USER_HOST}:{self.USER_PORT}/users"


settings = Setting()
