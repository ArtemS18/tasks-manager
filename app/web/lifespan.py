from contextlib import asynccontextmanager

from app.bd.connection import (
    connect as pg_connect, 
    disconnect as pg_disconnect
)

from fastapi import FastAPI
 
from app.email.connect import connect as email_connect

@asynccontextmanager
async def lifespan(app: "FastAPI"):
    pg_connect()
    email_connect()
    yield
    await pg_disconnect()
