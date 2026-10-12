from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./voting.db"
    admin_key: str = "community-admin"
    jwt_secret: str = "dev-only-change-me-before-production-use"
    jwt_expire_minutes: int = 60 * 24 * 7
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
