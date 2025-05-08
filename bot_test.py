import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = "7159421696:AAFPag8V0ayuGwXZWggduKfmcQXFp1xT9Lc"
CHANNEL_ID = -1001143201422  # Замените на ваш chat_id

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text="✅ Тестовое сообщение от бота!")
        print("✅ Сообщение успешно отправлено в канал.")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())