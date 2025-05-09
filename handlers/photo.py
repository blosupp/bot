# handlers/photo.py
from aiogram import Router, types
from config import ADMIN_ID
from services.openai_service import ask_gpt
from config import CHANNEL_ID

router = Router()

@router.message(lambda m: m.photo and m.caption)
async def handle_photo_with_caption(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔️ У тебя нет доступа к боту.")
        return

    await message.answer("🧠 Обрабатываю подпись через OpenAI...")

    try:
        result = ask_gpt(
            prompt=message.caption,
            system_prompt="Ты пишешь лаконичные Telegram-посты по теме изображения."
        )
        await message.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=message.photo[-1].file_id,
            caption=result
        )
        await message.answer("✅ Фото отправлено в канал.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
