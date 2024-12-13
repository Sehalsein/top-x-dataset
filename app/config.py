from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    version: str = "0.0.1"
    app_name: str = "case_study"

    redis_host: str = "localhost"
    redis_port: int = 6379

    kafka_bootstrap_server: str = "localhost:9092"

    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
