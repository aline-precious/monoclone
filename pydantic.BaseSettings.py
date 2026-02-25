"""Application configuration loaded from environment variables or .env file."""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central config for the application.
    All values can be overridden via environment variables or a .env file.
    """

    # ─── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str

    # ─── App ───────────────────────────────────────────────────────────────────
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    PROJECT_NAME: str = "Monoclone Order Management API"
    DEBUG: bool = False

    # ─── CORS ──────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # ─── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
