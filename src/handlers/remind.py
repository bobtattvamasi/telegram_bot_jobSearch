"""Handler for /remind command."""

from datetime import UTC, datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.storage import Storage

router = Router()


@router.message(Command("remind"))
async def handle_remind(message: Message, storage: Storage) -> None:
    """Handle /remind command to show stale applications.

    Args:
        message: Incoming Telegram message.
        storage: Storage dependency injected by dispatcher.
    """
    if message.from_user is None:
        await message.answer("❌ Не удалось определить пользователя.")
        return

    stale = await storage.get_stale_applications(user_id=message.from_user.id, days=7)

    if not stale:
        await message.answer("🎉 Все отклики актуальны!")
        return

    now = datetime.now(UTC)
    lines: list[str] = []
    for app in stale:
        updated = app.updated_at
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=UTC)
        else:
            updated = updated.astimezone(UTC)
        days_ago = (now - updated).days
        lines.append(f"📨 #{app.id} {app.company} — {app.position} — {days_ago}д назад")

    text = f"⚠️ Нет ответа более 7 дней ({len(stale)}):\n\n" + "\n".join(lines)
    await message.answer(text)
