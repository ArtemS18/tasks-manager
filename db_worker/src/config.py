import logging
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASEDIR = "env"

PATHENV = {"test": ".test.env", "dev": ".dev.env", "local": ".local.env"}


def get_path(env: str = "local", base_dir: str = BASEDIR):
    return base_dir + "/" + PATHENV[env]


class BaseConfig(BaseSettings):
    ENV_TYPE: str
    DEBUG: bool

    DATABASE_URL: str
    ECHO: bool

    DB_INTERVAL: str
    WORKER_INTERVAl: str

    class Config:
        env_file = get_path()
        extra = "ignore"


_config: BaseConfig | None = None


def setup_config(path: str = None, base_dir: str = BASEDIR) -> BaseConfig:
    global _config

    if env_type := os.environ.get("ENV_TYPE"):
        path = get_path(env_type, base_dir)

    if _config is None:
        load_dotenv(dotenv_path=path)
        env_file = path if path else get_path(base_dir=base_dir)
        logger.info("Config loaded from %s", env_file)
        _config = BaseConfig(_env_file=env_file)
    return _config


config = setup_config()
