# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import start, help  # импорты из твоих модулей


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
from handlers import start
dp.include_router(start.router)


# Регистрируем хендлеры
dp.include_router(start.router)
dp.include_router(help.router)

async def main():
    print("✅ Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())