from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.models import JobApplication, Status
from src.scheduler import check_ghosted, setup_scheduler


def make_app(app_id: int, user_id: int, days_ago: int = 15) -> JobApplication:
    now = datetime.now(UTC)
    ts = now - timedelta(days=days_ago)
    return JobApplication(
        id=app_id,
        user_id=user_id,
        company=f"Company{app_id}",
        position=f"Position{app_id}",
        url=None,
        status=Status.APPLIED,
        created_at=ts,
        updated_at=ts,
    )


async def test_check_ghosted_marks_stale_apps() -> None:
    app = make_app(app_id=1, user_id=123)

    storage = AsyncMock()
    storage.get_all_user_ids = AsyncMock(return_value=[123])
    storage.get_stale_applications = AsyncMock(return_value=[app])
    storage.update_status = AsyncMock(
        return_value=app.model_copy(update={"status": Status.GHOSTED})
    )

    bot = AsyncMock()
    bot.send_message = AsyncMock()

    await check_ghosted(storage, bot)

    storage.update_status.assert_awaited_once_with(
        user_id=123,
        app_id=1,
        new_status=Status.GHOSTED,
    )
    bot.send_message.assert_awaited_once()
    assert bot.send_message.call_args.kwargs["chat_id"] == 123


async def test_check_ghosted_no_stale_apps() -> None:
    storage = AsyncMock()
    storage.get_all_user_ids = AsyncMock(return_value=[123])
    storage.get_stale_applications = AsyncMock(return_value=[])
    storage.update_status = AsyncMock()

    bot = AsyncMock()
    bot.send_message = AsyncMock()

    await check_ghosted(storage, bot)

    storage.update_status.assert_not_called()
    bot.send_message.assert_not_called()


async def test_check_ghosted_handles_blocked_bot() -> None:
    app = make_app(app_id=2, user_id=123)

    storage = AsyncMock()
    storage.get_all_user_ids = AsyncMock(return_value=[123])
    storage.get_stale_applications = AsyncMock(return_value=[app])
    storage.update_status = AsyncMock(
        return_value=app.model_copy(update={"status": Status.GHOSTED})
    )

    bot = AsyncMock()
    bot.send_message = AsyncMock(side_effect=Exception("Forbidden: bot was blocked by the user"))

    await check_ghosted(storage, bot)

    storage.update_status.assert_awaited_once_with(
        user_id=123,
        app_id=2,
        new_status=Status.GHOSTED,
    )


async def test_check_ghosted_multiple_users() -> None:
    app_1 = make_app(app_id=10, user_id=123)
    app_2 = make_app(app_id=20, user_id=456)

    async def _get_stale(*, user_id: int, days: int) -> list[JobApplication]:
        assert days == 14
        if user_id == 123:
            return [app_1]
        if user_id == 456:
            return [app_2]
        return []

    storage = AsyncMock()
    storage.get_all_user_ids = AsyncMock(return_value=[123, 456])
    storage.get_stale_applications = AsyncMock(side_effect=_get_stale)
    storage.update_status = AsyncMock()

    bot = AsyncMock()
    bot.send_message = AsyncMock()

    await check_ghosted(storage, bot)

    assert bot.send_message.await_count == 2


def test_setup_scheduler_returns_scheduler() -> None:
    scheduler = setup_scheduler(AsyncMock(), AsyncMock(), reminder_hour=10)

    assert isinstance(scheduler, AsyncIOScheduler)
    assert len(scheduler.get_jobs()) >= 1


def test_setup_scheduler_job_configured() -> None:
    scheduler = setup_scheduler(AsyncMock(), AsyncMock(), reminder_hour=15)

    jobs = scheduler.get_jobs()
    assert len(jobs) >= 1
    job = jobs[0]
    trigger_repr = str(job.trigger)
    assert "hour='15'" in trigger_repr
