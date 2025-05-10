# handlers/photo.py

from aiogram import Router, types
from config import ADMIN_ID, CHANNEL_ID
from services.openai_service import ask_gpt
from aiogram import F

router = Router()

# 🧠 Хранилище истории сообщений
user_memory = {}  # user_id: list of messages (до 20)

@router.message(F.fhoto)
async def handle_photo_with_caption(message: types.Message):
    # ✅ Проверка на доступ только для ADMIN_ID
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("⛔️ Нет доступа.")
        return

    # ✅ Проверка на наличие подписи к фото
    if not message.caption:
        await message.answer("⚠️ Добавь подпись к фото — это будет темой поста.")
        return

    await message.answer("🧠 Обрабатываю изображение и подпись...")

    try:
        # ✅ Ограничивающий system_prompt для GPT
        system_prompt = (
            "Ты — Telegram-копирайтер. Пиши посты как подпись к фото. "
            "Не превышай 1024 символа. Без приветствий, без хэштегов, без лишнего. "
            "Никаких объяснений — только готовый, краткий, содержательный текст."
        )

        # 🧠 Обновляем историю диалога
        user_id = message.from_user.id
        user_memory.setdefault(user_id, []).append({"role": "user", "content": message.caption})

        # Оставляем только последние 20 сообщений
        if len(user_memory[user_id]) > 20:
            user_memory[user_id] = user_memory[user_id][-20:]

        # ✅ Генерация текста с контекстом
        gpt_reply = ask_gpt(
            prompt=message.caption,
            system_prompt=system_prompt,
            memory=user_memory[user_id]  # передаём историю
        )

        # 🧠 Добавляем ответ GPT в историю
        user_memory[user_id].append({"role": "assistant", "content": gpt_reply})

        # ✅ Страховка: обрезка текста если GPT нарушил лимит
        if len(gpt_reply) > 1024:
            gpt_reply = gpt_reply[:1021] + "..."

        # ✅ Отправка в канал
        await message.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=message.photo[-1].file_id,
            caption=gpt_reply,
            parse_mode="HTML"
        )

        # ✅ Подтверждение пользователю
        await message.answer("✅ Пост с изображением опубликован в канал.")

    except Exception as e:
        # ✅ Ловим и показываем ошибку
        await message.answer(f"❌ Ошибка при генерации поста: {e}")
