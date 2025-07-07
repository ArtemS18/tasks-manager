import logging
from taskiq_aio_pika import AioPikaBroker
from taskiq import TaskiqEvents, TaskiqState
from app.web.config import setup_config, get_config
import taskiq_fastapi


def setup_broker() -> AioPikaBroker:
    setup_config()
    config = get_config()
    broker = AioPikaBroker(config.rabbit.url)
    return broker


broker = setup_broker()

taskiq_fastapi.init(broker, "app.web.app:setup_app")

log = logging.getLogger(__name__)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState):
    log.info("SETUP WORKER")
