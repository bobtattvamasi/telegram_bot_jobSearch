from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

from src.handlers.status import handle_status
from src.models import JobApplication, Status
from src.storage import ApplicationNotFound


def make_message(text: str, user_id: int = 123) -> AsyncMock:
    message = AsyncMock()
    message.text = text
    message.from_user = MagicMock()
    message.from_user.id = user_id
    message.answer = AsyncMock()
    return message


def make_storage() -> AsyncMock:
    storage = AsyncMock()
    storage.update_status = AsyncMock(
        return_value=JobApplication(
            id=1,
            user_id=123,
            company="Trustana",
            position="AI Eng",
            url=None,
            status=Status.INTERVIEW,
            created_at=datetime(2025, 1, 1, tzinfo=UTC),
            updated_at=datetime(2025, 1, 2, tzinfo=UTC),
        )
    )
    return storage


async def test_status_update_success() -> None:
    message = make_message("/status 1 interview")
    storage = make_storage()

    await handle_status(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "🔄" in answer_text
    assert "INTERVIEW" in answer_text


async def test_status_not_found() -> None:
    message = make_message("/status 1 interview")
    storage = make_storage()
    storage.update_status = AsyncMock(side_effect=ApplicationNotFound("not found"))

    await handle_status(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "не найден" in answer_text


async def test_status_invalid_id() -> None:
    message = make_message("/status abc interview")
    storage = make_storage()

    await handle_status(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Использование" in answer_text


async def test_status_invalid_status() -> None:
    message = make_message("/status 1 invalid")
    storage = make_storage()

    await handle_status(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Доступные" in answer_text
    assert "applied" in answer_text
    assert "interview" in answer_text


async def test_status_missing_args() -> None:
    message = make_message("/status")
    storage = make_storage()

    await handle_status(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Использование" in answer_text
