from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Keys — empty means mock mode
    openai_api_key: str = ""
    tavily_api_key: str = ""

    # Database
    database_url: str = "postgresql+asyncpg://alphawatch:alphawatch@localhost:5432/alphawatch"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    @property
    def mock_mode(self) -> bool:
        return not self.openai_api_key or not self.tavily_api_key

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
