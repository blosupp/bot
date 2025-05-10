# handlers/photo.py

from aiogram import Router, types, F
from config import ADMIN_ID, CHANNEL_ID
from services.openai_service import ask_gpt
from db import save_message, load_history
from handlers.settings import user_settings

router = Router()

@router.message(F.photo)
async def handle_photo_with_caption(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("⛔️ Нет доступа.")
        return

    if not message.caption:
        await message.answer("⚠️ Добавь подпись к фото — это будет темой поста.")
        return

    await message.answer("🧠 Обрабатываю изображение и подпись...")

    try:
        uid = message.from_user.id
        remember = user_settings.get(uid, {}).get("remember", True)
        limit = user_settings.get(uid, {}).get("history_limit", 10)

        history = load_history(uid, limit)
        history.append({"role": "user", "content": message.caption})

        system_prompt = (
            "Ты — Telegram-копирайтер. Пиши посты как подпись к фото. "
            "Не превышай 1024 символа. Без приветствий, хэштегов, эмодзи и воды."
        )

        gpt_reply = ask_gpt(
            prompt=message.caption,
            system_prompt=system_prompt,
            memory=history
        )

        if remember:
            save_message(uid, "user", message.caption)
            save_message(uid, "assistant", gpt_reply)

        if len(gpt_reply) > 1024:
            gpt_reply = gpt_reply[:1021] + "..."

        await message.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=message.photo[-1].file_id,
            caption=gpt_reply,
            parse_mode="HTML"
        )

        await message.answer("✅ Пост с изображением опубликован в канал.")

    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {e}")