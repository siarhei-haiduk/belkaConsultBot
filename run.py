import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, SCHEDULE_INTERVAL
from app.user import user
from app.database.models import async_main
from app.scheduler import test_func


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test_func, trigger='interval', minutes=SCHEDULE_INTERVAL, kwargs={'bot': bot})  # Add job to check events
    scheduler.start()
    dp.include_routers(user)
    dp.startup.register(on_startup)


    await dp.start_polling(bot)


async def on_startup(dispatcher):
    await async_main()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


