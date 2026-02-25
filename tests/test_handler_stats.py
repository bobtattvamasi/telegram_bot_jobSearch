from unittest.mock import AsyncMock, MagicMock

from src.handlers.stats import handle_stats


def make_message(text: str = "/stats", user_id: int = 123) -> AsyncMock:
    message = AsyncMock()
    message.text = text
    message.from_user = MagicMock()
    message.from_user.id = user_id
    message.answer = AsyncMock()
    return message


async def test_stats_empty() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_stats = AsyncMock(return_value={"total": 0})

    await handle_stats(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Всего: 0" in answer_text


async def test_stats_with_data() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_stats = AsyncMock(return_value={"applied": 3, "interview": 1, "total": 4})

    await handle_stats(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "Applied: 3" in answer_text
    assert "Interview: 1" in answer_text
    assert "Всего: 4" in answer_text


async def test_stats_shows_all_statuses() -> None:
    message = make_message()
    storage = AsyncMock()
    storage.get_stats = AsyncMock(return_value={"total": 0})

    await handle_stats(message, storage)

    answer_text = message.answer.call_args.args[0]
    assert "📨" in answer_text
    assert "🔄" in answer_text
    assert "📝" in answer_text
    assert "✅" in answer_text
    assert "❌" in answer_text
    assert "👻" in answer_text
