from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ClientPilot"
    environment: str = "development"
    demo_mode: bool = True
    database_url: str = Field(
        default="postgresql+psycopg://clientpilot:clientpilot@localhost:5432/clientpilot"
    )
    llm_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"
    swytchcode_token: str | None = None
    swytchcode_bin: str = "swytchcode"
    swytchcode_project_dir: str = "."
    max_agent_iterations: int = Field(default=7, ge=1, le=8)


@lru_cache
def get_settings() -> Settings:
    return Settings()
