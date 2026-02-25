"""Handler for /delete command."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.storage import ApplicationNotFound, Storage

router = Router()

_USAGE_HINT = "Использование: /delete <id>"


@router.message(Command("delete"))
async def handle_delete(message: Message, storage: Storage) -> None:
    """Handle /delete <id> command.

    Args:
        message: Incoming Telegram message.
        storage: Storage dependency injected by dispatcher.
    """
    text = (message.text or "").strip()
    parts = text.split()

    if len(parts) != 2:
        await message.answer(_USAGE_HINT)
        return

    try:
        app_id = int(parts[1])
    except ValueError:
        await message.answer(_USAGE_HINT)
        return

    if message.from_user is None:
        await message.answer("❌ Не удалось определить пользователя.")
        return

    try:
        await storage.delete_application(user_id=message.from_user.id, app_id=app_id)
    except ApplicationNotFound:
        await message.answer(f"❌ Отклик #{app_id} не найден.")
        return
    except Exception:
        await message.answer("❌ Не удалось удалить отклик. Попробуйте позже.")
        return

    await message.answer(f"🗑 Отклик #{app_id} удалён.")
