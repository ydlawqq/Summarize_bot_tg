import asyncio

from sqlalchemy import text, insert, delete
from engine import engine
from engine import metadata_obj, workers_table




async def z():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT 'hello' "))
        print(res.all())

async def create_table():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE paper"))


asyncio.run(create_table())

