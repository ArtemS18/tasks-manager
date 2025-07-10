import logging
import sys
from taskiq_aio_pika import AioPikaBroker
from app.broker.tasks import setup_tasks
from app.web.config import setup_config
import taskiq_fastapi

from app.web.logger.setup import setup_logger_from_config


APP_PATH = "app.web.app:setup_app"

broker: AioPikaBroker | None = None


def setup_broker_in_a_worker_process() -> AioPikaBroker:
    config = setup_config()

    log: logging.Logger = setup_logger_from_config(config=config, file_name=__name__)
    log.info("Setup broker in worker proccess")

    broker = AioPikaBroker(config.rabbit.url)

    setup_tasks(broker)
    taskiq_fastapi.init(broker, APP_PATH)
    return broker


if sys.argv[0] == "worker":
    broker = setup_broker_in_a_worker_process()
