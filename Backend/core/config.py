from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    DB_HOST: str = Field(default=...)
    DB_PORT: int = Field(default=...)
    DB_USER: str = Field(default=...)
    DB_PASS: str = Field(default=...)
    DB_NAME: str = Field(default=...)
    SECRET_KEY: str = Field(default=...)
    ALGORITHM: str = Field(default=...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=...)
    REDIS_HOST: str = Field(default=...)
    REDIS_PORT: int = Field(default=...)
    ORIGINS: list[str] = Field(default=...) 

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

if os.environ.get("DB_HOST"):
    Settings.model_config["env_file"] = None
    settings = Settings()
else:
    settings = Settings()
