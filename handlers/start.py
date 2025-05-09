from aiogram import Router, types
from aiogram.filters import CommandStart
from config import ADMIN_ID

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        print(f"message.from_user.id: {message.from_user.id}, ADMIN_ID: {ADMIN_ID}")
        await message.answer("⛔️ У тебя нет доступа к этому боту.")
        return

    await message.answer("👋 Привет, босс.")
