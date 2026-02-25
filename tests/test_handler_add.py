from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

from src.handlers.add import handle_add
from src.models import JobApplication, Status


def make_message(text: str, user_id: int = 123) -> AsyncMock:
    message = AsyncMock()
    message.text = text
    message.from_user = MagicMock()
    message.from_user.id = user_id
    message.answer = AsyncMock()
    return message


def make_storage(app_id: int = 1) -> AsyncMock:
    storage = AsyncMock()
    storage.add_application = AsyncMock(
        return_value=JobApplication(
            id=app_id,
            user_id=123,
            company="TestCompany",
            position="TestPosition",
            url=None,
            status=Status.APPLIED,
            created_at=datetime(2025, 1, 15, tzinfo=UTC),
            updated_at=datetime(2025, 1, 15, tzinfo=UTC),
        )
    )
    return storage


async def test_add_with_company_and_position() -> None:
    message = make_message("/add Trustana LLM_Engineer")
    storage = make_storage()

    await handle_add(message, storage)

    storage.add_application.assert_awaited_once_with(
        user_id=123,
        company="Trustana",
        position="LLM_Engineer",
        url=None,
    )
    assert message.answer.called is True
    answer_text = message.answer.call_args.args[0]
    assert "✅" in answer_text


async def test_add_with_url() -> None:
    message = make_message("/add Trustana LLM_Engineer https://example.com")
    storage = make_storage()

    await handle_add(message, storage)

    storage.add_application.assert_awaited_once_with(
        user_id=123,
        company="Trustana",
        position="LLM_Engineer",
        url="https://example.com",
    )


async def test_add_with_quoted_args() -> None:
    message = make_message('/add "Statum Capital" "AI Engineer" https://example.com')
    storage = make_storage()

    await handle_add(message, storage)

    storage.add_application.assert_awaited_once_with(
        user_id=123,
        company="Statum Capital",
        position="AI Engineer",
        url="https://example.com",
    )


async def test_add_missing_args() -> None:
    message = make_message("/add")
    storage = make_storage()

    await handle_add(message, storage)

    storage.add_application.assert_not_called()
    assert message.answer.called is True
    answer_text = message.answer.call_args.args[0]
    assert "Использование" in answer_text


async def test_add_only_company() -> None:
    message = make_message("/add Trustana")
    storage = make_storage()

    await handle_add(message, storage)

    storage.add_application.assert_not_called()


async def test_add_response_contains_date() -> None:
    message = make_message("/add Test Dev")
    storage = make_storage()

    await handle_add(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "15.01.2025" in answer_text
