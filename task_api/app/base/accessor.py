from abc import ABC, abstractmethod
from app.lib.fastapi import FastAPI


class BaseAccessor(ABC):
    def __init__(self, app: "FastAPI", *args, **kwargs):
        self.app = app

    @abstractmethod
    async def connect(self):
        raise NotImplementedError()

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError()
