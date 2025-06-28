import typing

#from taskiq_aio_pika import AioPikaBroker
if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

class Store:
    def __init__(self, app: "FastAPI"):

        from app.store.bd.repository.tasks import TaskRepository
        from app.store.bd.repository.user import UserRepository

        self.user = UserRepository(app)
        self.task = TaskRepository(app)
        #self.broker = AioPikaBroker(app.config.AIOPIKA_URL)

        
def setup_store( app: "FastAPI"):
    app.store = Store(app)
