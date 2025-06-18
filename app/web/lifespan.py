from contextlib import asynccontextmanager

from app.bd.connection import (
    connect as pg_connect, 
    disconnect as pg_disconnect
)

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: "FastAPI"):
    pg_connect()
    yield
    pg_disconnect()
