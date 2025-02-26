from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.database.requests import get_user


async def main(tg_id):
    kb = ReplyKeyboardBuilder()
    user = await get_user(tg_id)
    if not user.consulted:
        kb.button(text='Консультация')
    if not user.portfolio:
        kb.button(text='Портфолио')
    if user.consulted & user.portfolio & user.contact_sent:
        kb.button(text='Вернуться на старт')
    return kb.as_markup(resize_keyboard=True, remove_keyboard=True)


consult = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Бесплатная консультация')]],  resize_keyboard=True)


async def contact(tg_id):
    kb = ReplyKeyboardBuilder()
    user = await get_user(tg_id)
    if not user.contact_sent:
        kb.button(text='Отправить свой контакт', request_contact=True)

    return kb.as_markup(resize_keyboard=True, remove_keyboard=True)
