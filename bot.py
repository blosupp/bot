import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Пример: -1001234567890

if not BOT_TOKEN or not OPENAI_API_KEY or not CHANNEL_ID:
    raise ValueError("❌ Проверь BOT_TOKEN, OPENAI_API_KEY и CHANNEL_ID в .env")

# Инициализация
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Привет! Напиши тему поста или прикрепи изображение с подписью — я всё опубликую в канал.")

# Текстовые сообщения
@dp.message(F.text)
async def generate_text_post(message: types.Message):
    user_input = message.text.strip()
    if not user_input:
        await message.answer("⚠️ Пожалуйста, укажи тему для поста.")
        return

    await message.answer("✍️ Генерирую пост...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": f"Сделай короткий пост в Telegram по теме: {user_input}"}
            ]
        )
        post_text = response.choices[0].message.content.strip()

        # Публикация текста в канал
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text)
        await message.answer("✅ Пост опубликован в канал.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# Фото с подписью
@dp.message(F.photo)
async def handle_photo_with_caption(message: types.Message):
    if not message.caption:
        await message.answer("⚠️ Пожалуйста, добавь подпись к фото — это будет темой поста.")
        return

    await message.answer("🧠 Обрабатываю изображение и подпись...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": f"Сделай Telegram-пост по теме: {message.caption}"}
            ]
        )
        post_text = response.choices[0].message.content.strip()

        # Публикация фото с текстом
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=message.photo[-1].file_id,
            caption=post_text,
            parse_mode="HTML"
        )

        await message.answer("✅ Пост с изображением опубликован в канал.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {e}")

# Запуск бота
async def main():
    print("✅ Бот запущен и готов.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())