from unittest.mock import AsyncMock, MagicMock

from aiogram.types import Message

from src.handlers.start import HELP_TEXT, handle_help, handle_start


async def test_handle_start_sends_welcome() -> None:
    message = AsyncMock(spec=Message)
    message.bot = MagicMock()
    message.answer = AsyncMock()

    await handle_start(message)

    assert message.answer.called is True
    called_text = message.answer.call_args.args[0]
    assert "/add" in called_text
    assert "/list" in called_text
    assert "/status" in called_text
    assert "/stats" in called_text
    assert "/remind" in called_text


async def test_handle_help_sends_same_text() -> None:
    message = AsyncMock(spec=Message)
    message.bot = MagicMock()
    message.answer = AsyncMock()

    await handle_help(message)

    message.answer.assert_called_once_with(HELP_TEXT)


def test_help_text_contains_all_commands() -> None:
    assert "/add" in HELP_TEXT
    assert "/list" in HELP_TEXT
    assert "/status" in HELP_TEXT
    assert "/delete" in HELP_TEXT
    assert "/stats" in HELP_TEXT
    assert "/remind" in HELP_TEXT


def test_help_text_is_in_russian() -> None:
    assert "отклик" in HELP_TEXT or "вакансии" in HELP_TEXT or "статус" in HELP_TEXT
