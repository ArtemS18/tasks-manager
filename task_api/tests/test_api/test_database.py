import pytest
from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncEngine

@pytest.mark.asyncio
async def test_bd(engine: AsyncEngine):
    from app.store.bd import models
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT 1"))
        assert res.scalar_one() == 1
    await engine.dispose()
