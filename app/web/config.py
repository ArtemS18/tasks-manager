from os import environ
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

_config: BaseSettings| None = None

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
    
    class Config:
        env_file = "env\.env"

def setup_config(env_path: str):
    global _config
    if _config is None:
        load_dotenv()
        _config = BaseConfig(_env_file=env_path)
    return _config


def get_config()->BaseConfig:
    if _config is None:
        raise RuntimeError("Config is not initialized")
    return _config

config = BaseConfig()

    

