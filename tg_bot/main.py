import asyncio
from src.bot.dispatcher import dp, polling
from src.bot.bot import bot


async def main():
    await polling(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())
