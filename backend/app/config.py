from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Keys — empty means mock mode
    anthropic_api_key: str = ""
    tavily_api_key: str = ""

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_ids: str = ""  # comma-separated chat IDs

    # Reddit
    reddit_client_id: str = ""
    reddit_client_secret: str = ""

    # Twitter
    twitter_bearer_token: str = ""

    # Database
    database_url: str = "postgresql+asyncpg://nexus:nexus@localhost:5432/nexus"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # Monitoring
    poll_interval_minutes: int = 10
    alert_relevance_threshold: float = 7.0

    @property
    def mock_mode(self) -> bool:
        return not self.anthropic_api_key

    @property
    def telegram_enabled(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_ids)

    @property
    def reddit_enabled(self) -> bool:
        return bool(self.reddit_client_id and self.reddit_client_secret)

    @property
    def twitter_enabled(self) -> bool:
        return bool(self.twitter_bearer_token)

    @property
    def chat_id_list(self) -> list[str]:
        if not self.telegram_chat_ids:
            return []
        return [cid.strip() for cid in self.telegram_chat_ids.split(",") if cid.strip()]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
