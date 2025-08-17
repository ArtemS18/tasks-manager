import logging
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASEDIR = "env"

PATHENV = {"test": ".test.env", "dev": ".dev.env", "local": ".local.env"}


def get_path(env: str = "local", base_dir: str = BASEDIR):
    return base_dir + "/" + PATHENV[env]


class ApiConfig(BaseModel):
    url: str = "http://localhost:8080/"
    token: str


class SiteConfig(BaseModel):
    url: str = "http://localhost:5173/"


class WebhookConfig(BaseModel):
    url: str
    host: str = "localhost"
    port: int = 80
    path: str = "webhook"


class RedisCondig(BaseModel):
    url: str = "redis://localhost:6379/1"
    username: str
    password: str


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=get_path(),
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="BOT__",
    )
    env_type: str = "local"
    token: str
    site: SiteConfig
    api: ApiConfig
    page_limit: int = 5
    webhook: WebhookConfig
    redis: RedisCondig


config: BaseConfig | None = None


def setup_config(path: str = None, base_dir: str = BASEDIR) -> BaseConfig:
    global config

    if env_type := os.environ.get("ENV_TYPE"):
        path = get_path(env_type, base_dir)

    if config is None:
        load_dotenv(dotenv_path=path)
        env_file = path if path else get_path(base_dir=base_dir)
        logger.info("Config loaded from %s", env_file)
        config = BaseConfig(_env_file=env_file)
    return config


config = setup_config()
