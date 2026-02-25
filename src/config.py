"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for bot runtime and reminder thresholds."""

    bot_token: str
    db_path: str = "data/tracker.db"
    log_level: str = "INFO"
    reminder_hour: int = 10
    reminder_days_threshold: int = 7
    ghosted_days_threshold: int = 14

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
