"""Scheduler setup and periodic ghosted-check jobs."""

import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore[import-untyped]

from src.models import Status
from src.storage import Storage


async def check_ghosted(storage: Storage, bot: Bot) -> None:
    """Check all users for ghosted applications and notify them.

    Args:
        storage: Storage layer instance.
        bot: Telegram bot instance for notifications.
    """
    user_ids = await storage.get_all_user_ids()

    for user_id in user_ids:
        stale_applications = await storage.get_stale_applications(user_id=user_id, days=14)

        for app in stale_applications:
            await storage.update_status(
                user_id=user_id,
                app_id=app.id,
                new_status=Status.GHOSTED,
            )

            text = (
                f"👻 #{app.id} {app.company} — {app.position} — "
                "автоматически помечен как GHOSTED (нет ответа 14+ дней)"
            )

            try:
                await bot.send_message(chat_id=user_id, text=text)
            except Exception:
                logging.warning(
                    "Could not deliver ghosted notification to user_id=%s for app_id=%s",
                    user_id,
                    app.id,
                )

            logging.info(
                "Application marked ghosted: user_id=%s app_id=%s company=%s position=%s",
                user_id,
                app.id,
                app.company,
                app.position,
            )


def setup_scheduler(storage: Storage, bot: Bot, reminder_hour: int = 10) -> AsyncIOScheduler:
    """Create and configure the scheduler.

    Args:
        storage: Storage layer instance.
        bot: Telegram bot instance for notifications.
        reminder_hour: Daily execution hour.

    Returns:
        Configured async scheduler.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_ghosted,
        trigger="cron",
        hour=reminder_hour,
        minute=0,
        kwargs={"storage": storage, "bot": bot},
    )
    return scheduler
