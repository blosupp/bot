# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import start, help, photo  # добавляй только один раз!

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ✅ Каждый router добавляется один раз
dp.include_router(start.router)
dp.include_router(help.router)
dp.include_router(photo.router)

async def main():
    print("✅ Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
