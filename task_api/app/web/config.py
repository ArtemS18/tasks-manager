import logging
from os import environ
import os
import typing
if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

logger= logging.getLogger(__name__)

BASEDIR = "env"

PATHENV = {
    'test': '.test.env',
    'dev': '.dev.env',
    'local': '.local.env'
}

def get_path(env: str = 'local', base_dir: str = BASEDIR):
    return base_dir + '/' + PATHENV[env]

class BaseConfig(BaseSettings):
    ENV_TYPE: str
    DEBUG: bool

    HOST: str
    PORT: int

    DATABASE_URL: str
    ECHO: bool

    JWT_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    JWT_REFRESH_EXPIRE_HOURS: int
    JWT_ALGORIM: str

    EMAIL_HOST:str
    EMAIL_PORT:str

    AIOPIKA_URL: str

    REDIS_URL: str
    REDIS_USERNAME: str
    REDIS_PASSWORD: str

    CONFIRM_PASSWORD_EXPIRE_MINUTES: int
    
    class Config:
        env_file = get_path()


config: BaseConfig | None = None

def setup_config(path: str = None, base_dir: str = BASEDIR) -> BaseConfig:
    global config

    if env_type:=os.environ.get("ENV_TYPE"):
        path = get_path(env_type, base_dir)

    if config is None:
        load_dotenv(dotenv_path=path)
        env_file = path if path else get_path(base_dir=base_dir)
        logger.info("Config loaded from %s", env_file)
        config = BaseConfig(_env_file=env_file)
    return config

def get_config(app: "FastAPI"):
    if config is None:
        setup_config()
    app.config = config

def get_current_config() -> BaseConfig:
    if config is None:
        raise RuntimeError("config not created")
    return config
