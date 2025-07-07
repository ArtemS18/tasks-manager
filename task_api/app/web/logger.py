import logging
import sys
import typing

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

LOGGER_LEVELS = {
    "test": "DEBUG",
    "local": "INFO",
    "dev": "INFO",
}

_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

_LONG_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] [%(processName)s] %(levelname)s %(module)10s:%(funcName)s:%(lineno)-3d %(message)s"

_BASE_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] %(levelname)s %(module)10s:%(funcName)s:%(lineno)-3d %(message)s"

_SHORT_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(message)s"

_WORKER_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] [%(processName)s] %(levelname)s %(module)10s:%(lineno)-3d %(message)s"


def setup_logger(app: "FastAPI", file_name: str = "web"):
    base_logger = logging.getLogger()
    base_logger.setLevel(LOGGER_LEVELS[app.config.env_type])

    handler = logging.StreamHandler()
    log_format = (
        _LONG_LOGGER_FORMAT if sys.argv[0] != "worker" else _WORKER_LOGGER_FORMAT
    )

    formatter = logging.Formatter(fmt=log_format, datefmt=_DATEFORMAT)
    handler.setFormatter(formatter)
    base_logger.addHandler(handler)

    app.logger = logging.getLogger(file_name)

    app.logger.info(
        f"Setup logger, loglevel = {logging.getLevelName(base_logger.level)}"
    )
