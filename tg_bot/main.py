import asyncio
import sys
from src.bot.dispatcher import dp, polling
from src.bot.bot import bot
from src.webhook.server import run_server


def main(_tupe: str):
    if _tupe == "web":
        run_server()
    elif _tupe == "poll":
        asyncio.run(polling(dp, bot))


if __name__ == "__main__":
    main(sys.argv[1])
    # asyncio.run(main())
