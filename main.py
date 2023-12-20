import logging
import asyncio 

from aiogram import Dispatcher, Router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from decouple import config

import handlers.other_functions as other_func
import mysql_connection as db

from handlers.callback_handlers import router as callback_router
from handlers.command_handlers import router as command_router
from handlers.message_handlers import router as message_router

# Set up logging
logging.basicConfig(
    filename='bot_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

bot = other_func.bot
dp = Dispatcher()
router = Router()


dp.include_routers(
    router,
    callback_router,
    command_router,
    message_router
)


async def main():
    await db.get_all_users_ids()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(other_func.donate_for_developer, "cron", day=25, hour=20)
    scheduler.add_job(db.get_all_users_ids, "interval", hours=1)
    scheduler.add_job(other_func.help_developer, "cron", day_of_week="tue", hour=20, minute=00)
    scheduler.add_job(other_func.check_log_file_and_send_to_developer, "cron", hour=22)
    scheduler.add_job(other_func.clear_log_file, "cron", hour=22, minute=1)
    scheduler.add_job(db.set_clickers_to_zero, "cron", hour=1)
    
    scheduler.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    

    
