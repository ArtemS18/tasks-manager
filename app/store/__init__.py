import typing

from app.store.redis.accessor import RedisAccessor

#from taskiq_aio_pika import AioPikaBroker
if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

class Store:
    def __init__(self, app: "FastAPI"):

        from app.store.bd.repository.tasks import TaskRepository
        from app.store.bd.repository.user import UserRepository

        self.user = UserRepository(app)
        self.task = TaskRepository(app)
        self.redis = RedisAccessor(app)
        #self.broker = AioPikaBroker(app.config.AIOPIKA_URL)

        
def setup_store( app: "FastAPI"):
    app.store = Store(app)