from aiogram import Router, types
from services.openai_service import ask_gpt
from db import save_message, load_history
from access import get_user_settings, get_user_channels, is_admin

router = Router()

user_contexts = {}  # user_id: {"mode": str, "history": list, "last_post": str}

CONFIRM_PHRASES = {"да", "публикуй", "отправляй", "ок"}
CANCEL_PHRASES = {"отмена", "не надо", "отменить"}
EDIT_PHRASES = {"измени", "перепиши", "доработай"}



def detect_intent(text: str) -> str:
    lowered = text.lower()
    if any(kw in lowered for kw in ["пост", "напиши", "опубликуй", "в канал", "опубликовать"]):
        return "post"
    return "dialog"

@router.message()
async def handle_ai(message: types.Message):
    uid = message.from_user.id
    text = message.text.strip()

    if not is_admin(uid):
        await message.answer("⛔️ У вас нет доступа.")
        return

    # Инициализируем контекст, если нет
    if uid not in user_contexts:
        user_contexts[uid] = {"mode": None, "history": [], "last_post": None}

    ctx = user_contexts[uid]

    # === ОБРАБОТКА ПОДТВЕРЖДЕНИЯ ===
    if ctx["mode"] == "confirm_post":
        if text.lower() in CONFIRM_PHRASES:
            channels = get_user_channels(uid)
            if not channels:
                await message.answer("⚠️ У вас не добавлен ни один канал.")
                ctx["mode"] = None
                return

            for ch in channels:
                await message.bot.send_message(
                    chat_id=ch,
                    text=ctx["last_post"],
                    parse_mode="HTML"
                )

            await message.answer("✅ Пост опубликован.")
            ctx["mode"] = None
            return

        elif text.lower() in CANCEL_PHRASES:
            ctx["mode"] = None
            await message.answer("❌ Публикация отменена.")
            return

        elif text.lower() in EDIT_PHRASES:
            ctx["mode"] = "edit_post"
            await message.answer("✏️ Введите новый вариант поста:")
            return

        else:
            await message.answer("🤖 Подтвердите: да / нет / изменить")
            return

    # === ОБРАБОТКА РУЧНОГО РЕДАКТИРОВАНИЯ ===
    if ctx["mode"] == "edit_post":
        new_post = text
        ctx["last_post"] = new_post
        ctx["mode"] = "confirm_post"
        await message.answer(f"📝 Новый пост:\n\n{new_post}\n\nПубликуем?")
        return

    # === ОПРЕДЕЛЕНИЕ РЕЖИМА ===
    intent = detect_intent(text)
    ctx["mode"] = intent

    # === ЗАГРУЗКА НАСТРОЕК ===
    user_data = get_user_settings(uid)
    remember = user_data["remember"]
    limit = user_data["history_limit"]

    if not ctx["history"]:
        ctx["history"] = load_history(uid, limit)

    ctx["history"].append({"role": "user", "content": text})

    # === PROMPT ===
    system_prompt = (
        "Ты — дружелюбный AI-ассистент в Telegram. Общайся с пользователем, веди диалог. "
        "Если он просит создать пост, сгенерируй краткий и чёткий текст без приветствий, эмодзи и хэштегов. "
        "Если вопрос личный — отвечай естественно."
    )

    try:
        reply = ask_gpt(prompt=text, system_prompt=system_prompt, memory=ctx["history"])

        if remember:
            save_message(uid, "user", text)
            save_message(uid, "assistant", reply)

        # === ДИАЛОГ ===
        if intent == "dialog":
            await message.answer(reply)
            ctx["history"].append({"role": "assistant", "content": reply})
            return

        # === ПОСТ ===
        if intent == "post":
            ctx["last_post"] = reply
            ctx["mode"] = "confirm_post"
            await message.answer(f"📋 Вот черновик поста:\n\n{reply}\n\nПубликуем? (да / нет / изменить)")
            return

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
