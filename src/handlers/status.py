"""Handler for /status command."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.models import Status
from src.storage import ApplicationNotFound, Storage

router = Router()

_USAGE_HINT = "Использование: /status <id> <new_status>"
_AVAILABLE_STATUSES = "applied, interview, test_task, offer, rejected, ghosted"


@router.message(Command("status"))
async def handle_status(message: Message, storage: Storage) -> None:
    """Handle /status <id> <new_status> command.

    Args:
        message: Incoming Telegram message.
        storage: Storage dependency injected by dispatcher.
    """
    text = (message.text or "").strip()
    parts = text.split()

    if len(parts) != 3:
        await message.answer(_USAGE_HINT)
        return

    raw_id = parts[1]
    raw_status = parts[2].lower()

    try:
        app_id = int(raw_id)
    except ValueError:
        await message.answer(_USAGE_HINT)
        return

    try:
        new_status = Status(raw_status)
    except ValueError:
        await message.answer("❌ Неизвестный статус. Доступные: " + _AVAILABLE_STATUSES)
        return

    if message.from_user is None:
        await message.answer("❌ Не удалось определить пользователя.")
        return

    try:
        updated = await storage.update_status(
            user_id=message.from_user.id,
            app_id=app_id,
            new_status=new_status,
        )
    except ApplicationNotFound:
        await message.answer(f"❌ Отклик #{app_id} не найден.")
        return
    except Exception:
        await message.answer("❌ Не удалось обновить статус. Попробуйте позже.")
        return

    await message.answer(
        f"🔄 #{updated.id} {updated.company} — {updated.position} — {updated.status.value.upper()}"
    )
