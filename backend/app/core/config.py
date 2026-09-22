from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = ROOT_DIR / "backend"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = Field(default="TripGenius")
    APP_ENV: str = Field(default="development")
    APP_DEBUG: bool = Field(default=True)

    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440)

    DATABASE_URL: str = Field(default="sqlite:///./tripgenius.db")

    TOURISM_DATASET_PATH: str = Field(default="database/tourism.csv")

    GEMINI_API_KEY: str
    OPENWEATHER_API_KEY: str

    CORS_ORIGINS: str = Field(default="http://localhost:3000")

    FRONTEND_URL: str = Field(default="http://localhost:3000")

    LOG_LEVEL: str = Field(default="INFO")

    @property
    def tourism_dataset_path(self) -> Path:
        dataset_path = ROOT_DIR / self.TOURISM_DATASET_PATH

        if not dataset_path.exists():
            raise FileNotFoundError(f"Tourism dataset not found: {dataset_path}")

        return dataset_path

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]

    @property
    def sqlite_database_file(self) -> Path:
        if self.DATABASE_URL.startswith("sqlite:///"):
            database_name = self.DATABASE_URL.replace("sqlite:///", "")
            return BACKEND_DIR / database_name

        return BACKEND_DIR / "tripgenius.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
