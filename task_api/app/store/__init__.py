import typing

#from taskiq_aio_pika import AioPikaBroker
if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

class Store:
    def __init__(self, app: "FastAPI"):

        from app.store.bd.repository.tasks import TaskRepository
        from app.store.bd.repository.user import UserRepository
        from app.store.email.accessor import SMTPAccessor
        from app.store.redis.accessor import RedisAccessor

        self.user = UserRepository(app)
        self.task = TaskRepository(app)
        self.redis = RedisAccessor(app)
        self.smtp = SMTPAccessor(app)

    async def connect_all(self):
        for name, attr in vars(self).items():
            if hasattr(attr, "connect") and callable(getattr(attr, "connect")):
                await attr.connect()
    async def disconnect_all(self):
        for name, attr in vars(self).items():
            if hasattr(attr, "disconnect") and callable(getattr(attr, "disconnect")):
                await attr.disconnect()

def setup_store( app: "FastAPI"):
    app.store = Store(app)