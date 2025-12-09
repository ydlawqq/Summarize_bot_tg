from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from HOTEL.Postgres.models import Users
from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert
import datetime
from HOTEL.Postgres.models import Chat

class UserRepos:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_user(self, **kwargs):
        telegram_id = kwargs.get('telegram_id')
        stmt = insert(Users).values(**kwargs).on_conflict_do_update(index_elements=[Users.telegram_id], set_={
            'last_seen': datetime.datetime.now(datetime.timezone.utc)
        })
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_by_tg_id(self, tg_id):
        user = await self.session.execute(select(Users).where(
            Users.telegram_id==tg_id
        ))
        return user.scalars().first()





