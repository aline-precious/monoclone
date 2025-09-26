from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()


#Database and session initialization need settings.DATABASE_URL, 
# so the settings must be defined before you create the DB engine or sessionmaker.

