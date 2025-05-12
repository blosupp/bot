from aiogram import Router, types, F
from services.openai_service import ask_gpt
from db import save_message, load_history
from access import get_user_settings, get_user_channels, is_admin
import re

router = Router()
pending_photos = {}

CAPTION_LIMIT = 1024

def truncate_caption(text: str, max_len: int = 1024) -> tuple[str, str | None]:
    plain_text = re.sub(r"<[^>]+>", "", text)
    if len(plain_text) <= max_len:
        return plain_text, None
    return plain_text[:max_len - 3] + "...", plain_text[max_len - 3:]

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

        preview, continuation = truncate_caption(gpt_reply, CAPTION_LIMIT)

        pending_photos[uid] = {
            "photo_id": message.photo[-1].file_id,
            "caption": preview,
            "continuation": continuation
        }

        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="✅ Публиковать", callback_data="photo_publish_confirm"),
                types.InlineKeyboardButton(text="❌ Отменить", callback_data="photo_publish_cancel")
            ]
        ])

        await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=f"🤖 Вот черновик подписи:\n\n{preview}",
            reply_markup=kb,
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {e}")

@router.callback_query(F.data.in_({"photo_publish_confirm", "photo_publish_cancel"}))
async def handle_photo_publish(callback: types.CallbackQuery):
    uid = callback.from_user.id

    if uid not in pending_photos:
        await callback.message.answer("⚠️ Нет подготовленного поста.")
        return

    if callback.data == "photo_publish_cancel":
        pending_photos.pop(uid)
        await callback.message.delete()
        await callback.message.answer("❌ Публикация отменена.")
        return

    if callback.data == "photo_publish_confirm":
        post = pending_photos.pop(uid)
        channels = get_user_channels(uid)

        if not channels:
            await callback.message.answer("⚠️ У вас не добавлен ни один канал.")
            return

        for ch_id in channels:
            await callback.bot.send_photo(
                chat_id=ch_id,
                photo=post["photo_id"],
                caption=post["caption"],
                parse_mode="HTML"
            )
            if post["continuation"]:
                button = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="📖 Читать ещё", callback_data="photo_continue_text")]
                ])
                await callback.bot.send_message(
                    chat_id=ch_id,
                    text="⏩ Продолжение поста доступно по кнопке ниже:",
                    reply_markup=button
                )

                # Сохраняем continuation для callback
                pending_photos[uid] = {"continuation_only": post["continuation"]}

        await callback.message.delete()
        await callback.message.answer("✅ Пост с изображением опубликован в ваши каналы.")

@router.callback_query(F.data == "photo_continue_text")
async def send_continuation(callback: types.CallbackQuery):
    uid = callback.from_user.id
    if uid not in pending_photos or "continuation_only" not in pending_photos[uid]:
        await callback.answer("⚠️ Продолжение не найдено.", show_alert=True)
        return

    continuation = pending_photos[uid].pop("continuation_only")
    await callback.message.answer(f"📎 Продолжение:{continuation}")
