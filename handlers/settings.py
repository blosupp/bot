from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(Command("settings"))
async def settings_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 GPT: Включить", callback_data="toggle_gpt")],
        [InlineKeyboardButton(text="📂 Категория: Новости", callback_data="set_category_news")],
        [InlineKeyboardButton(text="📅 Отложить пост", callback_data="schedule_post")],
    ])
    await message.answer("⚙️ Настройки бота:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("toggle_gpt"))
async def toggle_gpt(callback: types.CallbackQuery):
    await callback.answer("🧠 GPT включён (заглушка)")
    await callback.message.edit_text("✅ GPT включён", reply_markup=None)

@router.callback_query(F.data.startswith("set_category_news"))
async def set_category(callback: types.CallbackQuery):
    await callback.answer("📂 Категория: Новости выбрана")
    await callback.message.edit_text("✅ Категория выбрана: Новости", reply_markup=None)

@router.callback_query(F.data.startswith("schedule_post"))
async def schedule_post(callback: types.CallbackQuery):
    await callback.answer("🕐 В будущем тут будет планировщик публикации")
    await callback.message.edit_text("🔧 Планирование пока в разработке", reply_markup=None)
