import logging
from fastapi import FastAPI, Request, Response

logger = logging.getLogger(__name__)

async def exeption_middlewary(request: Request, call_next):
    try:
        logger.info(request.headers.items())
        response: Response = await call_next(request)
        logger.info(response.headers.items())
    except Exception as e:
        logger.error(e)
    finally:
        return response


def setup_middlewary(app: "FastAPI"):
    app.middleware('http')(exeption_middlewary)
    
