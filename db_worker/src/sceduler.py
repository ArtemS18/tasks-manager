import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.scripts.check_date import cleanup_users
from src.config import config

logger = logging.getLogger(__name__)

intevals = dict(p.split("_")[::-1] for p in config.WORKER_INTERVAl.split())
JOB_CLEANUP_INTERVAL = {k: int(v) for k, v in intevals.items()}


async def setup_scheduler():
    scheduler = AsyncIOScheduler()
    logger.info(f"Interval {JOB_CLEANUP_INTERVAL}")
    scheduler.add_job(cleanup_users, trigger=IntervalTrigger(**JOB_CLEANUP_INTERVAL))
    scheduler.start()
    # await cleanup_users(config.DB_INTERVAL)
