import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка токенов
if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Укажи BOT_TOKEN и OPENAI_API_KEY в .env файле!")

# Инициализация
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Привет! Напиши что-нибудь, и я спрошу у GPT 🤖")

# Ответ на любое сообщение
@dp.message()
async def handle_message(message: types.Message):
    user_input = message.text
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # можно заменить на "gpt-3.5-turbo"
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Ошибка: {e}"
    await message.answer(reply)

# Запуск бота
async def main():
    print("✅ Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())