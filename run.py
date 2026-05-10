from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import TOKEN
from app.handlers import router
from app.profile_handlers import profile_router
from app.database import init_db

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    # Инициализация баз данных
    init_db()
    logging.info("Базы данных инициализированы")
    
    dp.include_router(router)
    dp.include_router(profile_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
