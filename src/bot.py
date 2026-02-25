"""Bot entry point and dispatcher setup."""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config import Settings
from src.handlers.add import router as add_router
from src.handlers.start import router as start_router
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
    dp["storage"] = storage

    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
