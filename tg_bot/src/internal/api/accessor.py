from aiohttp import ClientSession

from src.bot.config import config
from src.models.task import Task


async def send() -> Task:
    async with ClientSession() as session:
        async with session.get(
            config.api.url + "/internal/",
            headers={"X-Internal-Token": config.api.token},
        ) as response:
            data = await response.json()
            return Task.model_validate(data["tasks"][0])
