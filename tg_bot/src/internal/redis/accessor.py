from redis.asyncio import Redis
from src.config import config
from aiogram.fsm.state import State


class RedisAccessor:
    def __init__(self):
        self.redis: Redis | None = None

    async def connect(self):
        self.redis = Redis.from_url(
            url=config.redis.url,
            password=config.redis.password,
            decode_responses=True,
        )

    async def disconnect(self):
        if self.redis is not None:
            await self.redis.aclose()

    def get_client(self) -> Redis:
        client = self.redis
        if client is not None:
            return client

    async def set_page_data(self, base_key: str, state: str, page: int, data: str):
        key = f"{base_key}:{state}:{page}"
        await self.redis.set(key, data, ex=60)

    async def get_page_data(self, base_key: str, state: str, page: int) -> str:
        key = f"{base_key}:{state}:{page}"
        res = await self.redis.get(key)
        return res


redis = Redis.from_url(
    url=config.redis.url,
    password=config.redis.password,
    decode_responses=True,
)
redis_api = RedisAccessor()
