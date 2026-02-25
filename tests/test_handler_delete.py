from unittest.mock import AsyncMock, MagicMock

from src.handlers.delete import handle_delete
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
    storage.delete_application = AsyncMock(return_value=True)
    return storage


async def test_delete_success() -> None:
    message = make_message("/delete 1")
    storage = make_storage()

    await handle_delete(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "удалён" in answer_text


async def test_delete_not_found() -> None:
    message = make_message("/delete 1")
    storage = make_storage()
    storage.delete_application = AsyncMock(side_effect=ApplicationNotFound("not found"))

    await handle_delete(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "не найден" in answer_text


async def test_delete_invalid_id() -> None:
    message = make_message("/delete abc")
    storage = make_storage()

    await handle_delete(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Использование" in answer_text


async def test_delete_missing_args() -> None:
    message = make_message("/delete")
    storage = make_storage()

    await handle_delete(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Использование" in answer_text
