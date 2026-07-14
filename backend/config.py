from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "voicetag-shop-fastapi"
    debug: bool = False
    database_url: str = Field(
        default="sqlite+aiosqlite:///./shop.db",
        examples=["sqlite+aiosqlite:///./shop.db"],
    )
    cors_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
