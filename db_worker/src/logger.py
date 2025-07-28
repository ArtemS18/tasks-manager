from .config import config
from logging import (
    Formatter,
    getLogger, 
    StreamHandler, 
)
LEVELS = {
    "test": "DEBUG",
    "dev": "INFO",
    "local": "INFO"
}

def setup_logger():
    logger = getLogger()
    logger.setLevel(LEVELS[config.ENV_TYPE])
    formattter = Formatter("[%(asctime)s][%(levelname)s][%(name)s]%(message)s")
    handler = StreamHandler()
    handler.setFormatter(formattter)
    logger.addHandler(handler)
    