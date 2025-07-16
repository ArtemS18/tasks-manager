from redis.asyncio import Redis

from app.base.accessor import BaseAccessor
from app.lib.fastapi import FastAPI


class RedisAccessor(BaseAccessor):
    def __init__(self, app: "FastAPI"):
        super().__init__(app)
        self.redis: Redis | None = None

    async def connect(self):
        self.redis = Redis.from_url(
            url=self.app.config.redis.url,
            password=self.app.config.redis.password,
            decode_responses=True,
        )

    async def disconnect(self):
        if self.redis is not None:
            await self.redis.aclose()

    async def create_confirming_password(
        self, user_id: int, password: str, expire_seconds: int = None
    ):
        if expire_seconds is None:
            expire_seconds = self.app.config.jwt.confirm_expire * 60
        await self.redis.set(user_id, password, ex=expire_seconds)

    async def get_confirming_password(self, user_id: int):
        password = await self.redis.get(user_id)
        return password
