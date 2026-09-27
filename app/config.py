from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PocketSmart AI"

    SECRET_KEY: str = "change-this-secret-key"

    DATABASE_URL: str = "sqlite:///./pocketsmart.db"

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.5-flash"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    MAX_UPLOAD_MB: int = 5

    CORS_ORIGINS: str = (
        "http://127.0.0.1:8000,"
        "http://localhost:8000"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_list(self):
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings():
    return Settings()