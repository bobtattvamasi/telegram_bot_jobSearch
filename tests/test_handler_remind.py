from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from src.handlers.remind import handle_remind
from src.models import JobApplication, Status


def make_message(text: str = "/remind", user_id: int = 123) -> AsyncMock:
    message = AsyncMock()
    message.text = text
    message.from_user = MagicMock()
    message.from_user.id = user_id
    message.answer = AsyncMock()
    return message


def make_app(app_id: int, company: str, days_ago: int) -> JobApplication:
    now = datetime.now(UTC)
    updated = now - timedelta(days=days_ago)
    return JobApplication(
        id=app_id,
        user_id=123,
        company=company,
        position="Dev",
        url=None,
        status=Status.APPLIED,
        created_at=updated,
        updated_at=updated,
    )


async def test_remind_no_stale() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_stale_applications = AsyncMock(return_value=[])

    await handle_remind(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Все отклики актуальны" in answer_text


async def test_remind_with_stale() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_stale_applications = AsyncMock(
        return_value=[
            make_app(app_id=1, company="Trustana", days_ago=10),
            make_app(app_id=2, company="Acme", days_ago=8),
        ]
    )

    await handle_remind(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Trustana" in answer_text
    assert "Acme" in answer_text


async def test_remind_shows_days() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_stale_applications = AsyncMock(
        return_value=[make_app(app_id=1, company="Trustana", days_ago=12)]
    )

    await handle_remind(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "д назад" in answer_text
