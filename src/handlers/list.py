"""Handler for /list command."""

from datetime import UTC, datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.models import Status
from src.storage import Storage

router = Router()

EMOJI_MAP: dict[Status, str] = {
    Status.APPLIED: "📨",
    Status.INTERVIEW: "🔄",
    Status.TEST_TASK: "📝",
    Status.OFFER: "✅",
    Status.REJECTED: "❌",
    Status.GHOSTED: "👻",
}

_INVALID_STATUS_TEXT = (
    "❌ Неизвестный статус. Доступные: applied, interview, test_task, offer, rejected, ghosted"
)


@router.message(Command("list"))
async def handle_list(message: Message, storage: Storage) -> None:
    """Handle /list command to display job applications.

    Args:
        message: Incoming Telegram message.
        storage: Storage dependency injected by dispatcher.
    """
    if message.from_user is None:
        await message.answer("❌ Не удалось определить пользователя.")
        return

    text = (message.text or "").strip()
    parts = text.split(maxsplit=1)

    status_filter: Status | None = None
    if len(parts) > 1 and parts[1].strip():
        raw_status = parts[1].strip().lower()
        try:
            status_filter = Status(raw_status)
        except ValueError:
            await message.answer(_INVALID_STATUS_TEXT)
            return

    applications = await storage.get_applications(
        user_id=message.from_user.id,
        status_filter=status_filter,
    )

    if not applications:
        await message.answer("📋 Список пуст. Используй /add чтобы добавить отклик.")
        return

    now = datetime.now(UTC)
    lines: list[str] = []

    for app in applications:
        days_ago = (now - app.updated_at.astimezone(UTC)).days
        emoji = EMOJI_MAP.get(app.status, "📌")
        line = (
            f"{emoji} #{app.id} {app.company} — {app.position} — "
            f"{app.status.value.upper()} ({days_ago}д назад)"
        )
        if app.status is Status.APPLIED and days_ago > 7:
            line += " ⚠️"
        lines.append(line)

    result = f"📋 Мои отклики ({len(applications)}):\n\n" + "\n".join(lines)
    await message.answer(result)
