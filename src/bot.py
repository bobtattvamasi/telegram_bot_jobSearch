"""Bot entry point and dispatcher setup."""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config import Settings
from src.handlers.add import router as add_router
from src.handlers.delete import router as delete_router
from src.handlers.fallback import router as fallback_router
from src.handlers.list import router as list_router
from src.handlers.remind import router as remind_router
from src.handlers.start import router as start_router
from src.handlers.stats import router as stats_router
from src.handlers.status import router as status_router
from src.scheduler import setup_scheduler
from src.storage import Storage


async def main() -> None:
    """Initialize application services and start bot polling."""
    settings = Settings()  # type: ignore[call-arg]

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    storage = Storage(settings.db_path)
    await storage.init_db()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(add_router)
    dp.include_router(list_router)
    dp.include_router(status_router)
    dp.include_router(delete_router)
    dp.include_router(stats_router)
    dp.include_router(remind_router)
    dp.include_router(fallback_router)
    dp["storage"] = storage

    scheduler = setup_scheduler(storage, bot, settings.reminder_hour)
    scheduler.start()
    logging.info("Scheduler started")
    logging.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
