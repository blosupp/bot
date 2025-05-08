from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio

bot = Bot(token="7159421696:AAFPag8V0ayuGwXZWggduKfmcQXFp1xT9Lc")
dp = Dispatcher()

@dp.channel_post()
async def catch_channel_post(message: Message):
    await bot.send_message(chat_id=message.chat.id, text=f"✅ Channel ID: {message.chat.id}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())