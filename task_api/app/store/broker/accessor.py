import typing
from app.base.accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI
    from taskiq_aio_pika import AioPikaBroker


class BrokerAccessor(BaseAccessor):
    def __init__(self, app: "FastAPI", broker: "AioPikaBroker"):
        super().__init__(app)
        self.broker = broker

    async def connect(self):
        if not self.broker.is_worker_process:
            await self.broker.startup()

    async def disconnect(self):
        if not self.broker.is_worker_process:
            await self.broker.shutdown()
