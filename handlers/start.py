# handlers/start.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from config import ADMIN_ID

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):

    print(f"[DEBUG] from_user.id = {message.from_user.id}, ADMIN_ID = {ADMIN_ID}")

    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔️ У тебя нет доступа.")
        return
    await message.answer("👋 Привет, босс.")
