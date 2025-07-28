import logging
from sqlalchemy import text
from db.connect import engin
from src.config import config

logger= logging.getLogger(__name__)

async def cleanup_users():
    interval = config.DB_INTERVAL
    query = text(
        "DELETE FROM users WHERE users.status = 'pending'"
        f" AND users.created_at < NOW() - INTERVAL '{interval}'"
    )
    logger.info(f"Start cleanup_users, interval: {interval}")
    async with engin.connect() as conn:
        async with conn.begin():
            res = await conn.execute(query)
            deleted = res.rowcount
    logger.info(f"Stop cleanup_users deleted: {deleted}")

