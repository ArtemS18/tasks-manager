import logging
from fastapi import FastAPI, Request, Response

logger = logging.getLogger(__name__)

async def exeption_middlewary(request: Request, call_next):
    try:
        response: Response = await call_next(request)
        return response
    except Exception as e:
        logger.error(e)


def setup_middlewary(app: "FastAPI"):
    pass
    #app.middleware('http')(exeption_middlewary)
    
