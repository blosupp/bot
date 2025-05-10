# handlers/admin_panel.py

from aiogram import Router, F, types
from aiogram.filters import Command
from access import is_admin, add_user, remove_user, add_channel, remove_channel, get_user_channels

router = Router()

pending_actions = {}  # user_id: (action, role)

# Главное меню
@router.message(Command("доступ"))
async def access_menu(message: types.Message):
    if not is_admin(str(message.from_user.id)):
        await message.answer("⛔️ Только для админов.")
        return

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="add_user"),
            types.InlineKeyboardButton(text="❌ Удалить пользователя", callback_data="remove_user")
        ],
        [
            types.InlineKeyboardButton(text="📡 Добавить канал", callback_data="add_channel"),
            types.InlineKeyboardButton(text="🗑 Удалить канал", callback_data="remove_channel")
        ],
        [
            types.InlineKeyboardButton(text="📋 Мои каналы", callback_data="list_channels")
        ]
    ])
    await message.answer("⚙️ Панель управления:", reply_markup=kb)

# Обработка кнопок
@router.callback_query(F.data.in_(
    ["add_user", "remove_user", "add_channel", "remove_channel", "list_channels"]
))
async def handle_access_buttons(callback: types.CallbackQuery):
    uid = str(callback.from_user.id)
    action = callback.data

    if not is_admin(uid):
        await callback.answer("⛔️ Нет доступа.", show_alert=True)
        return

    if action == "list_channels":
        channels = get_user_channels(uid)
        text = "📋 Ваши каналы:\n" + ("\n".join(channels) if channels else "(Пусто)")
        await callback.message.answer(text)
        await callback.answer()
        return

    prompt_map = {
        "add_user": "✏️ Введите user_id для ДОБАВЛЕНИЯ:",
        "remove_user": "✏️ Введите user_id для УДАЛЕНИЯ:",
        "add_channel": "✏️ Введите channel_id для ДОБАВЛЕНИЯ:",
        "remove_channel": "✏️ Введите channel_id для УДАЛЕНИЯ:",
    }
    pending_actions[uid] = action
    await callback.message.answer(prompt_map[action])
    await callback.answer()

# Обработка следующего сообщения
@router.message()
async def handle_pending_input(message: types.Message):
    uid = str(message.from_user.id)

    if uid not in pending_actions:
        return  # обычное сообщение

    action = pending_actions.pop(uid)
    target = message.text.strip()

    try:
        if action == "add_user":
            add_user(user_id=target, role="user", added_by=uid)
            await message.answer("✅ Пользователь добавлен.")
        elif action == "remove_user":
            remove_user(user_id=target)
            await message.answer("✅ Пользователь удалён.")
        elif action == "add_channel":
            add_channel(channel_id=target, owner_id=uid)
            await message.answer("✅ Канал добавлен.")
        elif action == "remove_channel":
            remove_channel(channel_id=target, owner_id=uid)
            await message.answer("✅ Канал удалён.")
        else:
            await message.answer("⚠️ Неизвестное действие.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
