from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import TOKEN
from app.handlers import router
from app.profile_handlers import profile_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    dp.include_router(profile_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
