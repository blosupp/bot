from aiogram import Router, types, F
from services.openai_service import ask_gpt
from db import save_message, load_history
from access import get_user_settings, get_user_channels, is_admin

router = Router()

@router.message(F.photo)
async def handle_photo_with_caption(message: types.Message):
    uid = message.from_user.id

    if not is_admin(uid):
        await message.answer("⛔️ Нет доступа.")
        return

    if not message.caption:
        await message.answer("⚠️ Добавь подпись к фото — это будет темой поста.")
        return

    await message.answer("🧠 Обрабатываю изображение и подпись...")

    try:
        user_data = get_user_settings(uid)
        remember = user_data["remember"]
        limit = user_data["history_limit"]

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

        channels = get_user_channels(uid)
        if not channels:
            await message.answer("❗️ У вас не добавлен ни один канал.")
            return

        for ch_id in channels:
            await message.bot.send_photo(
                chat_id=ch_id,
                photo=message.photo[-1].file_id,
                caption=gpt_reply,
                parse_mode="HTML"
            )

        await message.answer("✅ Пост с изображением опубликован в ваши каналы.")

    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {e}")
