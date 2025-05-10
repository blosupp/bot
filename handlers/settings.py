from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()
user_settings = {}  # user_id: {"remember": True, "history_limit": 10}

def get_settings_kb(user_id):
    remember = user_settings.get(user_id, {}).get("remember", True)
    limit = user_settings.get(user_id, {}).get("history_limit", 10)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🧠 Запоминать: {'✅' if remember else '❌'}", callback_data="toggle_remember")],
        [InlineKeyboardButton(text=f"📚 История: {limit}", callback_data="set_limit")]
    ])

@router.message(Command("настройки"))
async def show_settings(message: types.Message):
    kb = get_settings_kb(message.from_user.id)
    await message.answer("⚙️ Настройки бота:", reply_markup=kb)

@router.callback_query(F.data == "toggle_remember")
async def toggle_remember(cb: types.CallbackQuery):
    uid = cb.from_user.id
    current = user_settings.get(uid, {}).get("remember", True)
    user_settings.setdefault(uid, {})["remember"] = not current
    await cb.message.edit_reply_markup(reply_markup=get_settings_kb(uid))
    await cb.answer("🔁 Обновлено")

@router.callback_query(F.data == "set_limit")
async def set_limit(cb: types.CallbackQuery):
    uid = cb.from_user.id
    current = user_settings.get(uid, {}).get("history_limit", 10)
    new_limit = 5 if current == 20 else current + 5
    user_settings.setdefault(uid, {})["history_limit"] = new_limit
    await cb.message.edit_reply_markup(reply_markup=get_settings_kb(uid))
    await cb.answer(f"📚 Лимит: {new_limit}")
