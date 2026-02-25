from unittest.mock import AsyncMock

from src.handlers.fallback import handle_unknown


async def test_unknown_message_returns_hint() -> None:
    message = AsyncMock()
    message.answer = AsyncMock()

    await handle_unknown(message)

    assert message.answer.called
    assert "/help" in message.answer.call_args[0][0]


async def test_unknown_message_is_friendly() -> None:
    message = AsyncMock()
    message.answer = AsyncMock()

    await handle_unknown(message)

    text = message.answer.call_args[0][0]
    assert "🤔" in text
