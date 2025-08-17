import asyncio
import sys
from src.bot.dispatcher import setup_dispatcher, polling
from src.bot import setup_bot
from src.bot.webhook.server import run_server


def main():
    bot = setup_bot()
    dp = setup_dispatcher()

    command = None if len(sys.argv) < 2 else sys.argv[1]

    match command:
        case "web":
            run_server(dp, bot)
        case "poll":
            asyncio.run(polling(dp, bot))
        case None:
            asyncio.run(polling(dp, bot))


if __name__ == "__main__":
    main()
    # asyncio.run(main())
