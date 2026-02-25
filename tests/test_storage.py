from datetime import UTC, datetime, timedelta

import aiosqlite
import pytest

from src.models import Status
from src.storage import ApplicationNotFound, Storage


async def test_init_db_creates_table(storage: Storage) -> None:
    async with aiosqlite.connect(storage._db_path) as db:  # noqa: SLF001
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='applications'"
        )
        row = await cursor.fetchone()

    assert row is not None
    assert row[0] == "applications"


async def test_add_application_success(storage: Storage) -> None:
    app = await storage.add_application(
        user_id=1,
        company="Acme",
        position="Backend Engineer",
        url="https://example.com",
    )

    assert app.id > 0
    assert app.user_id == 1
    assert app.company == "Acme"
    assert app.position == "Backend Engineer"
    assert app.url == "https://example.com"
    assert app.status == Status.APPLIED


async def test_add_application_without_url(storage: Storage) -> None:
    app = await storage.add_application(user_id=1, company="NoURL", position="Developer")

    assert app.url is None


async def test_get_applications_empty(storage: Storage) -> None:
    applications = await storage.get_applications(user_id=999)

    assert applications == []


async def test_get_applications_returns_user_apps(storage: Storage) -> None:
    await storage.add_application(user_id=1, company="A", position="Dev")
    await storage.add_application(user_id=1, company="B", position="QA")

    applications = await storage.get_applications(user_id=1)

    assert len(applications) == 2
    assert all(app.user_id == 1 for app in applications)


async def test_get_applications_filter_by_status(storage: Storage) -> None:
    first = await storage.add_application(user_id=1, company="A", position="Dev")
    second = await storage.add_application(user_id=1, company="B", position="QA")
    await storage.update_status(user_id=1, app_id=second.id, new_status=Status.INTERVIEW)

    interview_only = await storage.get_applications(user_id=1, status_filter=Status.INTERVIEW)

    assert len(interview_only) == 1
    assert interview_only[0].id == second.id
    assert interview_only[0].status == Status.INTERVIEW
    assert all(app.id != first.id for app in interview_only)


async def test_update_status_success(storage: Storage) -> None:
    app = await storage.add_application(user_id=1, company="Acme", position="Dev")

    updated = await storage.update_status(user_id=1, app_id=app.id, new_status=Status.INTERVIEW)

    assert updated.id == app.id
    assert updated.status == Status.INTERVIEW


async def test_update_status_not_found(storage: Storage) -> None:
    with pytest.raises(ApplicationNotFound):
        await storage.update_status(user_id=1, app_id=999, new_status=Status.INTERVIEW)


async def test_update_status_wrong_user(storage: Storage) -> None:
    app = await storage.add_application(user_id=1, company="Acme", position="Dev")

    with pytest.raises(ApplicationNotFound):
        await storage.update_status(user_id=2, app_id=app.id, new_status=Status.INTERVIEW)


async def test_delete_application_success(storage: Storage) -> None:
    app = await storage.add_application(user_id=1, company="Acme", position="Dev")

    deleted = await storage.delete_application(user_id=1, app_id=app.id)
    remaining = await storage.get_applications(user_id=1)

    assert deleted is True
    assert remaining == []


async def test_delete_application_not_found(storage: Storage) -> None:
    with pytest.raises(ApplicationNotFound):
        await storage.delete_application(user_id=1, app_id=999)


async def test_get_stale_applications(storage: Storage) -> None:
    app = await storage.add_application(user_id=1, company="Acme", position="Dev")
    stale_time = datetime.now(UTC) - timedelta(days=10)

    async with aiosqlite.connect(storage._db_path) as db:  # noqa: SLF001
        await db.execute(
            "UPDATE applications SET updated_at = ? WHERE id = ?",
            (stale_time.isoformat(), app.id),
        )
        await db.commit()

    stale = await storage.get_stale_applications(user_id=1, days=7)

    assert len(stale) == 1
    assert stale[0].id == app.id


async def test_get_stats_empty(storage: Storage) -> None:
    stats = await storage.get_stats(user_id=1)

    assert stats["total"] == 0


async def test_get_stats_with_data(storage: Storage) -> None:
    first = await storage.add_application(user_id=1, company="A", position="Dev")
    second = await storage.add_application(user_id=1, company="B", position="QA")
    third = await storage.add_application(user_id=1, company="C", position="SRE")

    await storage.update_status(user_id=1, app_id=second.id, new_status=Status.INTERVIEW)
    await storage.update_status(user_id=1, app_id=third.id, new_status=Status.REJECTED)

    stats = await storage.get_stats(user_id=1)

    assert stats["applied"] == 1
    assert stats["interview"] == 1
    assert stats["rejected"] == 1
    assert stats["total"] == 3
    assert first.id > 0
