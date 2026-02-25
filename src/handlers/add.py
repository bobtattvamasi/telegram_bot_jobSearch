"""Handler for /add command."""

import shlex

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.storage import Storage

router = Router()

USAGE_HINT = (
    "Использование: /add <компания> <позиция> [url]\n"
    'Пример: /add "Statum Capital" "AI Engineer" https://example.com'
)


@router.message(Command("add"))
async def handle_add(message: Message, storage: Storage) -> None:
    """Handle /add command to create a new job application.

    Args:
        message: Incoming Telegram message.
        storage: Storage dependency injected by dispatcher.
    """
    text = message.text or ""
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(USAGE_HINT)
        return

    args_text = parts[1]

    try:
        args = shlex.split(args_text)
    except ValueError:
        await message.answer(USAGE_HINT)
        return

    if len(args) < 2:
        await message.answer(USAGE_HINT)
        return

    company = args[0]
    position = args[1]
    url = args[2] if len(args) >= 3 else None

    if message.from_user is None:
        await message.answer("Не удалось определить пользователя. Попробуйте ещё раз.")
        return

    try:
        application = await storage.add_application(
            user_id=message.from_user.id,
            company=company,
            position=position,
            url=url,
        )
    except Exception:
        await message.answer("Не удалось добавить отклик. Попробуйте позже.")
        return

    date_str = application.created_at.strftime("%d.%m.%Y")
    await message.answer(
        f"✅ #{application.id} {application.company} — "
        f"{application.position} — APPLIED ({date_str})"
    )
