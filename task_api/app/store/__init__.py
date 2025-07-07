import logging
import typing

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

logger = logging.getLogger("web")


class Store:
    def __init__(self, app: "FastAPI"):
        self.app = app

        from app.store.bd.repository.tasks import TaskRepository
        from app.store.bd.repository.user import UserRepository
        from app.store.email.accessor import SMTPAccessor
        from app.store.redis.accessor import RedisAccessor
        from app.store.broker.accessor import BrokerAccessor
        from app.broker import broker

        self.user = UserRepository(app)
        self.task = TaskRepository(app)
        self.redis = RedisAccessor(app)
        self.smtp = SMTPAccessor(app)
        self.broker = BrokerAccessor(app, broker)

    async def connect_all(self):
        for name, attr in vars(self).items():
            if hasattr(attr, "connect") and callable(getattr(attr, "connect")):
                await attr.connect()
                self.app.logger.info(f"Connected to {name}")

    async def disconnect_all(self):
        for name, attr in vars(self).items():
            if hasattr(attr, "disconnect") and callable(getattr(attr, "disconnect")):
                await attr.disconnect()
                self.app.logger.info(f"Disconnected to {name}")


def setup_store(app: "FastAPI"):
    app.store = Store(app)
    logger.info("Setup store")
