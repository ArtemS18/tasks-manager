from aioredis import from_url, Redis

from app.entity.user import User
from app.lib.fastapi import FastAPI

class RedisAccessor:
    def __init__(self, app: "FastAPI"):
        self.app = app
        self.redis: Redis | None = None

    async def connect(self):
        self.redis = await from_url(
            url=self.app.config.REDIS_URL,
            password=self.app.config.REDIS_PASSWORD,
            decode_responses=True,
        )

    async def disconnect(self):
        if self.redis is not None:
            await self.redis.close()

    async def create_confirming_password(self, user_id: int, password: str, expire_seconds: int = None):
        if expire_seconds is None:
            expire_seconds=self.app.config.CONFIRM_PASSWORD_EXPIRE_MINUTES*60
        await self.redis.set(user_id, password,  ex=expire_seconds)

    async def get_confirming_password(self, user_id: int):
        password = await self.redis.get(user_id)
        return password



