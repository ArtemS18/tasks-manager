from typing import TypedDict


LONG_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] [%(processName)s] %(levelname)s %(module)10s:%(funcName)s:%(lineno)-3d %(message)s"

BASE_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] %(levelname)s %(module)10s:%(funcName)s:%(lineno)-3d %(message)s"

SHORT_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(message)s"

WORKER_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] [%(processName)s] %(levelname)s %(module)10s:%(funcName)s:%(lineno)-3d %(message)s"

DATEFORMAT = "%Y-%m-%d %H:%M:%S"

LOGGERS_TYPE_FORMAT = {
    "worker": WORKER_LOGGER_FORMAT,
    "dev": LONG_LOGGER_FORMAT,
    "local": BASE_LOGGER_FORMAT,
    "test": SHORT_LOGGER_FORMAT,
}
LOGGER_LEVELS = {"test": "DEBUG", "local": "INFO", "dev": "INFO", "worker": "INFO"}


class LogEnvConfig(TypedDict):
    logLevel: str
    formatter: str
    dateformat: str


class LogEnvFormatters:
    worker = LogEnvConfig(
        logLevel="INFO", formatter=WORKER_LOGGER_FORMAT, dateformat=DATEFORMAT
    )
    dev = LogEnvConfig(
        logLevel="INFO", formatter=LONG_LOGGER_FORMAT, dateformat=DATEFORMAT
    )
    local = LogEnvConfig(
        logLevel="INFO", formatter=BASE_LOGGER_FORMAT, dateformat=DATEFORMAT
    )
    test = LogEnvConfig(
        logLevel="DEBUG", formatter=SHORT_LOGGER_FORMAT, dateformat=DATEFORMAT
    )
