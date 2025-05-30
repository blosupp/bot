import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from db import init_db
from access import init_access_db
from middleware.access_control import AccessMiddleware

from handlers import start, help, photo, post, settings, admin_panel, text
from access import add_user


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.message.middleware(AccessMiddleware())

dp.include_router(start.router)
dp.include_router(help.router)
# dp.include_router(post.router)
dp.include_router(photo.router)
dp.include_router(settings.router)
dp.include_router(admin_panel.router)
dp.include_router(text.router)


async def main():
    init_db()
    init_access_db()
    print("✅ Бот запущен и готов к работе.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
