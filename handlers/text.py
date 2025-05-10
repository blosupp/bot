from aiogram import Router, types
from config import ADMIN_ID, CHANNEL_ID
from services.openai_service import ask_gpt
from db import save_message, load_history
from handlers.settings import user_settings

router = Router()

@router.message()
async def handle_text(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("⛔️ Нет доступа.")
        return

    prompt = message.text.strip()
    if not prompt:
        await message.answer("⚠️ Пустое сообщение.")
        return

    await message.answer("✍️ Генерирую пост...")

    try:
        uid = message.from_user.id
        remember = user_settings.get(uid, {}).get("remember", True)
        limit = user_settings.get(uid, {}).get("history_limit", 10)
        history = load_history(uid, limit)
        history.append({"role": "user", "content": prompt})

        system_prompt = (
            "Ты — Telegram-копирайтер. Пиши посты по запросу пользователя. "
            "Не добавляй приветствий, хэштегов и эмодзи. Максимум — 1024 символа. Пиши чётко и по делу."
        )

        gpt_reply = ask_gpt(
            prompt=prompt,
            system_prompt=system_prompt,
            memory=history
        )

        if remember:
            save_message(uid, "user", prompt)
            save_message(uid, "assistant", gpt_reply)

        await message.bot.send_message(
            chat_id=CHANNEL_ID,
            text=gpt_reply,
            parse_mode="HTML"
        )

        await message.answer("✅ Пост опубликован в канал.")

    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {e}")