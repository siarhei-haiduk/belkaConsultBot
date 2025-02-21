from typing import Any

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedColumn
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: MappedColumn[Any] = mapped_column(BigInteger)
    time: Mapped[datetime] = mapped_column(nullable=True, default=None)
    consulted: Mapped[bool] = mapped_column(default=False)
    portfolio: Mapped[bool] = mapped_column(default=False)
    contact_sent: Mapped[bool] = mapped_column(default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

