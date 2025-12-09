from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from HOTEL.Postgres.models import Chat



class HistoryMessages:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_message(self, **kwargs):
        user_id = kwargs.get('id')
        stmt = insert(Chat).values(**kwargs)
        await self.session.execute(stmt)

    async def get_history_by_id(self, id)-> list[dict[str, str]]:

        stmt = select(Chat.role, Chat.content).where(Chat.user_id==id)
        result = await self.session.execute(stmt)
        return [{role: content} for role, content in result.fetchall()]

