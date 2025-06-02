import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

environment = os.getenv("PYTHON_ENV", "development")


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    automa_webhook_secret: str = "atma_whsec_bot-python"


@lru_cache
def env():
    return Config()
