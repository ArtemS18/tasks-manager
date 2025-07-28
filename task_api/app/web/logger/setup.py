import logging
from logging import Formatter, Logger
from app.web.config import BaseConfig
from app.web.logger import const
from app.lib.fastapi import FastAPI


def setup_logger_formatter(name: str) -> Formatter:
    log_format = const.LOGGERS_TYPE_FORMAT[name]
    formatter = Formatter(fmt=log_format, datefmt=const.DATEFORMAT)
    return formatter


def setup_logger(app: FastAPI, file_name: str = "web"):
    base_logger = logging.getLogger()
    if base_logger.hasHandlers():
        app.logger = logging.getLogger(file_name)
        app.logger.warning("Logger already setup")
        return
    base_logger.setLevel(const.LOGGER_LEVELS[app.config.env_type])

    handler = logging.StreamHandler()
    formatter = setup_logger_formatter(app.config.env_type)
    handler.setFormatter(formatter)
    base_logger.addHandler(handler)
    app.logger = logging.getLogger(file_name)

    app.logger.info(
        f"Setup logger, loglevel = {logging.getLevelName(base_logger.level)}"
    )


def setup_logger_from_config(config: BaseConfig, file_name: str = "worker") -> Logger:
    base_logger = logging.getLogger()
    if base_logger.hasHandlers():
        logger = logging.getLogger(file_name)
        logger.warning("Logger already setup")
        return logger
    base_logger.setLevel(const.LOGGER_LEVELS[config.env_type])

    handler = logging.StreamHandler()
    formatter = setup_logger_formatter(config.env_type)
    handler.setFormatter(formatter)
    base_logger.addHandler(handler)
    return logging.getLogger(file_name)
