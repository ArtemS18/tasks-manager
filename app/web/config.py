from os import environ
import typing
if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

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
    
    class Config:
        env_file = "env\.env"


config: BaseConfig | None = None

def setup_config(path: str = "env\.env") -> BaseConfig:
    global config
    if config is None:
        load_dotenv()
        config = BaseConfig(_env_file=path)
    return config

def get_config(app: "FastAPI"):
    if config is None:
        setup_config()
    app.config = config

def get_current_config() -> BaseConfig:
    if config is None:
        raise RuntimeError("config not created")
    return config
