import asyncio, logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from data.config_reader import bot_token
from db.model import async_upd_model
from handlers.users import start, shedule, verification, help, unknown
from handlers.adm import admin
from interval_command.change_numerator import change_numerator
from middlewares.ban_middleware import UserBannedMiddleware

# Регистрация мидлверов
def register_middlewares(dp: Dispatcher):
    dp.message.middleware(UserBannedMiddleware())

# Регистрация роутеров
def register_handlers(dp: Dispatcher):
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(shedule.router)
    dp.include_router(verification.router)
    dp.include_router(unknown.router)

# Стартовая функция
async def main():
    # Upd schemas in DB
    await async_upd_model()
    
    # Create instance Bot | Dispatcher | AsyncIOScheduler
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()
    
    # registration middlewares & handlers
    register_middlewares(dp)
    register_handlers(dp)
    
    # add jobs for Scheduler 
    scheduler.add_job(
        func=change_numerator, 
        trigger='cron',
        timezone='Europe/Moscow',
        day_of_week="sun"
    )
    
    # Start working
    try:
        scheduler.start()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f'[Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print("bot is over")