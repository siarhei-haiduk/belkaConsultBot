from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from config import ADMIN_CHAT_ID, PDF_PATH, TEXT1, TEXT2, TEXT4, MENTION_INTERVAL
import app.keyboards as kb
from app.states import ContactMe
from app.database.requests import set_user, user_consulted, user_portfolio_sent, user_contact_sent

user = Router()


@user.message(CommandStart(), F.chat.type == 'private')
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await set_user(message.from_user.id, time=None)
    await message.answer(text=TEXT1, parse_mode='html', reply_markup=await kb.main(message.from_user.id))


@user.message(F.text.lower() == 'консультация')
@user.message(F.text.lower() == 'бесплатная консультация')
async def cmd_consult(message: Message, state: FSMContext):
    await user_consulted(message.from_user.id)
    await message.answer(text=TEXT4, parse_mode='html', reply_markup=await kb.contact(message.from_user.id))
    await state.set_state(ContactMe.message)


@user.message(ContactMe.message)
async def forward_contact(message: Message, state: FSMContext):
    await user_contact_sent(message.from_user.id)
    await message.answer(text=TEXT2, parse_mode='html', reply_markup=await kb.main(message.from_user.id))
    await message.bot.send_message(chat_id=ADMIN_CHAT_ID, text='Поступил новый запрос на консультацию:')
    await message.send_copy(chat_id=ADMIN_CHAT_ID)
    await state.clear()


@user.message(F.text.lower() == 'портфолио')
async def cmd_portfolio(message: Message):
    await message.answer_document(document=FSInputFile(path=PDF_PATH), reply_markup=await kb.main(message.from_user.id))
    await user_portfolio_sent(tg_id=message.from_user.id, time=datetime.now() + timedelta(seconds=MENTION_INTERVAL))

