from logging import Logger
from fastapi import (
    FastAPI as LibFastApi,
    Request as LibRequest,
    WebSocket as WebSocketLib,
)


class FastAPI(LibFastApi):
    def __init__(self, *args, **kwargs):
        from app.store import Store
        from app.web.config import BaseConfig

        self.config: BaseConfig | None = None
        self.store: Store | None = None
        self.logger: Logger | None = None
        super().__init__(*args, **kwargs)


class Request(LibRequest):
    def __init__(self, scope, *args, **kwargs):
        super().__init__(scope, *args, **kwargs)

    @property
    def app(self) -> FastAPI:
        super().app


class WebSocket(WebSocketLib):
    @property
    def app(self) -> FastAPI:
        super().app
