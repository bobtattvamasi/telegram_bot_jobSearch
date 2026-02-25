from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from src.handlers.list import handle_list
from src.models import JobApplication, Status


def make_message(text: str = "/list", user_id: int = 123) -> AsyncMock:
    message = AsyncMock()
    message.text = text
    message.from_user = MagicMock()
    message.from_user.id = user_id
    message.answer = AsyncMock()
    return message


def make_app(
    app_id: int = 1,
    status: Status = Status.APPLIED,
    days_ago: int = 0,
    company: str = "TestCo",
    position: str = "Dev",
) -> JobApplication:
    now = datetime.now(UTC)
    ts = now - timedelta(days=days_ago)
    return JobApplication(
        id=app_id,
        user_id=123,
        company=company,
        position=position,
        url=None,
        status=status,
        created_at=ts,
        updated_at=ts,
    )


async def test_list_empty() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_applications = AsyncMock(return_value=[])

    await handle_list(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Список пуст" in answer_text


async def test_list_with_applications() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_applications = AsyncMock(
        return_value=[
            make_app(app_id=1, company="Trustana", position="AI Eng"),
            make_app(app_id=2, company="Acme", position="Dev"),
        ]
    )

    await handle_list(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Trustana" in answer_text
    assert "Acme" in answer_text
    assert "📋 Мои отклики (2)" in answer_text


async def test_list_filtered_by_status() -> None:
    message = make_message("/list interview")
    storage = AsyncMock()
    storage.get_applications = AsyncMock(return_value=[make_app(status=Status.INTERVIEW)])

    await handle_list(message, storage)

    storage.get_applications.assert_awaited_once_with(
        user_id=123,
        status_filter=Status.INTERVIEW,
    )


async def test_list_invalid_status() -> None:
    message = make_message("/list invalid_status")
    storage = AsyncMock()
    storage.get_applications = AsyncMock(return_value=[])

    await handle_list(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Неизвестный статус" in answer_text
    storage.get_applications.assert_not_called()


async def test_list_stale_warning() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_applications = AsyncMock(
        return_value=[make_app(days_ago=10, status=Status.APPLIED)]
    )

    await handle_list(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "⚠️" in answer_text


async def test_list_no_warning_for_recent() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_applications = AsyncMock(
        return_value=[make_app(days_ago=2, status=Status.APPLIED)]
    )

    await handle_list(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "⚠️" not in answer_text


async def test_list_emoji_mapping() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_applications = AsyncMock(return_value=[make_app(status=Status.INTERVIEW)])

    await handle_list(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "🔄" in answer_text
