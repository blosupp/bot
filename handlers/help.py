# handlers/help.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("ℹ️ Это бот, который помогает публиковать посты в канал с помощью ИИ.")