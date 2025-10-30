import logging
from logging import Formatter, Logger, getLogger
import os
from typing import Literal

from flask import json
from app.web.config import BaseConfig
from app.web.logger import const
from app.lib.fastapi import FastAPI
from logging_loki import LokiHandler

LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100/loki/api/v1/push")
LIB_LOGGERS = ["uvicorn.access", "fastapi", "uvicorn.error", "starlette"]

FormatterType = Literal["worker", "dev", "local", "test"]


def setup_logger_formatter(
    command: FormatterType,
) -> Formatter:
    log_format = const.LOGGERS_TYPE_FORMAT[command]
    formatter = Formatter(fmt=log_format, datefmt=const.DATEFORMAT)
    return formatter


def setup_loki_handler(logger: Logger, *, loki_url: str):
    loki_handler = LokiHandler(
        url=loki_url,
        tags={
            "app": "task_api",
            "env": "dev",
            "service_name": "fastapi",
            "worker": str(os.getenv("APP__WEB__WORKERS", 1)),
        },
        version="1",
    )
    loki_formatter = setup_logger_formatter("dev")
    loki_handler.setFormatter(loki_formatter)

    logger.addHandler(loki_handler)

    for _log in LIB_LOGGERS:
        lib_logger = getLogger(_log)
        lib_logger.setLevel("INFO")
        lib_logger.addHandler(loki_handler)


def setup_stream_handler(logger: Logger, type: FormatterType = "local"):
    handler = logging.StreamHandler()
    formatter = setup_logger_formatter(type)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def setup_logger(app: FastAPI, file_name: str = "web"):
    base_logger = logging.getLogger()

    if base_logger.hasHandlers():
        app.logger = logging.getLogger(file_name)
        app.logger.warning("Logger already setup")
        return
    base_logger.setLevel(const.LOGGER_LEVELS[app.config.env_type])

    setup_stream_handler(base_logger)
    setup_loki_handler(base_logger, loki_url=LOKI_URL)
    base_logger.info("Setup loki handler url = %s", LOKI_URL)

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
