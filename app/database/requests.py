from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def set_user(session, tg_id, time):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, time=time))
    else:
        await session.execute(update(User).where(User.tg_id == tg_id).values(time=None, consulted=False,
                                                                             portfolio=False, contact_sent=False))

    await session.commit()


@connection
async def user_contact_sent(session, tg_id):
    await session.execute(update(User).where(User.tg_id == tg_id).values(contact_sent=True))

    await session.commit()


@connection
async def user_consulted(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id))
    else:
        await session.execute(update(User).where(User.tg_id == tg_id).values(consulted=True))

    await session.commit()


@connection
async def user_portfolio_sent(session, tg_id, time):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, time=time, portfolio=True))
    else:
        await session.execute(update(User).where(User.tg_id == tg_id).values(time=time, portfolio=True))

    await session.commit()


@connection
async def get_user(session, tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))


@connection
async def get_users(session, time):
    return await session.scalars(select(User).where((User.time!= None) & (User.time <= time)))



