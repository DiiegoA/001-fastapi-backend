from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")
    DEBUG: bool = Field(default=False, env="DEBUG")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    LOG_LEVEL: str = Field(default="DEBUG", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings()
