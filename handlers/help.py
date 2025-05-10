from aiogram import Router, types
from aiogram.filters import Command
from access import is_admin, is_superadmin

router = Router()

@router.message(Command("myid"))
async def cmd_myid(message: types.Message):
    await message.answer(f"🆔 Ваш Telegram ID: <code>{message.from_user.id}</code>", parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    uid = message.from_user.id
    commands = [
        "🟢 <b>/start</b> — начать работу с ботом",
        "🧠 <b>/help</b> — показать список команд",
        "📌 <b>/myid</b> — узнать свой Telegram ID"
    ]

    if is_admin(uid):
        commands += [
            "\n<b>👨‍💼 Админ-команды:</b>",
            "⚙️ <b>/доступ</b> — панель управления каналами и пользователями"
        ]

    if is_superadmin(uid):
        commands += [
            "\n<b>👑 Суперадмин-команды:</b>",
            "🆙 <b>/add_admin &lt;id&gt;</b> — добавить админа",
            "📋 <b>/list_users</b> — список всех пользователей и ролей"
        ]

    await message.answer("\n".join(commands), parse_mode="HTML")
