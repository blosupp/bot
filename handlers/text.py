from aiogram import Router, types
from config import CHANNEL_ID
from services.openai_service import ask_gpt
from db import save_message, load_history
from access import get_user_settings, get_user_channels, is_admin

router = Router()

@router.message()
async def handle_text(message: types.Message):
    uid = message.from_user.id
    print(f"[TEXT] Сообщение от {uid}: {message.text}")
    if not is_admin(uid):
        await message.answer("⛔️ Нет доступа.")
        return

    prompt = message.text.strip()
    if not prompt:
        await message.answer("⚠️ Пустое сообщение.")
        return

    await message.answer("✍️ Генерирую пост...")

    try:
        user_data = get_user_settings(uid)
        remember = user_data["remember"]
        limit = user_data["history_limit"]

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

        channels = get_user_channels(uid)
        if not channels:
            await message.answer("❗️ У вас не добавлен ни один канал.")
            return

        for ch_id in channels:
            await message.bot.send_message(
                chat_id=ch_id,
                text=gpt_reply,
                parse_mode="HTML"
            )

        await message.answer("✅ Пост опубликован в ваши каналы.")

    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {e}")
