# handlers/text.py
from aiogram import Router, types
from config import ADMIN_ID
from services.openai_service import ask_gpt

router = Router()

@router.message()
async def handle_text(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔️ Нет доступа.")
        return

    prompt = message.text.strip()
    if not prompt:
        await message.answer("⚠️ Пустое сообщение.")
        return

    await message.answer("✍️ Думаю...")

    try:
        reply = ask_gpt(prompt)
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
