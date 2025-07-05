import logging
import typing

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

LOGGER_LEVELS = {
    'test': "DEBUG",
    'local': "INFO",
    'dev': 'INFO',
}

def setup_logger(app: "FastAPI", file_name: str = "web"):
    base_logger = logging.getLogger()
    base_logger.setLevel(LOGGER_LEVELS[app.config.env_type])

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s]%(message)s")
    handler.setFormatter(formatter)
    base_logger.addHandler(handler)

    app.logger = logging.getLogger(file_name)

    app.logger.info(f"Setup logger, loglevel = {logging.getLevelName(base_logger.level)}")
    

