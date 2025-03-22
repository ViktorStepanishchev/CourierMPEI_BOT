import logging, asyncio, sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from common.middlewares.db import DataBaseSession
from database.engine import create_db, session_maker

from handlers import router

from config import TOKEN

async def main() -> None:

    dp = Dispatcher()
    bot = Bot(token=TOKEN)
    bot.default.parse_mode = ParseMode.HTML

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    dp.update.middleware(DataBaseSession(session_pool = session_maker))

    await create_db()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())