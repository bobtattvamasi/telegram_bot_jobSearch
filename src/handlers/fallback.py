"""Fallback handler for unknown messages."""

from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def handle_unknown(message: Message) -> None:
    """Reply to any unrecognized message with a hint.

    Args:
        message: Incoming Telegram message.
    """
    await message.answer(
        "🤔 Не понимаю команду. Введите /help чтобы посмотреть список доступных команд."
    )
