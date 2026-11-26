from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    ADMIN_EMAIL: str | None = None
    ADMIN_PASSWORD: str | None = None

    model_config=SettingsConfigDict(
        env_file=".env"
    )
settings=Settings()
