import logging
import os
import typing

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASEDIR = "env"

PATHENV = {"test": ".test.env", "dev": ".dev.env", "local": ".local.env"}


def get_path(env: str = "local", base_dir: str = BASEDIR):
    return base_dir + "/" + PATHENV[env]


class WebConig(BaseModel):
    host: str = "localhost"
    port: int = 8080
    workers: int = 1
    reload: bool = False


class InternalConfig(BaseModel):
    token: str | None = None


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False


class JwtConfig(BaseModel):
    access_expire: int
    secret_key: str
    refresh_expire: int
    algorithm: str
    confirm_expire: int


class SmtpConfig(BaseModel):
    host: str = "localhost"
    port: int = 1025
    tls: bool = False
    remote_connect: bool = False
    email: str = "root@localhost.com"
    password: str | None = None


class RabbitConfig(BaseModel):
    url: str


class RedisConfig(BaseModel):
    url: str
    username: str
    password: str


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=get_path(),
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="APP__",
    )
    env_type: str = "local"
    web: WebConig
    db: DatabaseConfig
    jwt: JwtConfig
    smtp: SmtpConfig
    rabbit: RabbitConfig
    redis: RedisConfig
    internal: InternalConfig


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


def get_app_config(app: "FastAPI"):
    if config is None:
        setup_config()
    app.config = config


def get_config() -> BaseConfig:
    if config is None:
        raise RuntimeError("config not created")
    return config
