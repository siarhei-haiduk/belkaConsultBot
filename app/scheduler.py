from aiogram import Bot
from datetime import datetime

from config import TEXT3
from app.database.requests import get_users, user_consulted
import app.keyboards as kb

async def test_func(bot: Bot):
    users = await get_users(datetime.now())

    for user in users:
        if not user.consulted:
            await bot.send_message(chat_id=user.tg_id, text=TEXT3, parse_mode='html', reply_markup=kb.consult)
            await user_consulted(user.tg_id)
