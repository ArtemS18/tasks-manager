import asyncio
from src.logger import setup_logger
from src.sceduler import setup_scheduler


async def main():
    setup_logger()
    await setup_scheduler()

    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass