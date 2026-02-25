"""Handlers for /start and /help commands."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()

HELP_TEXT = (
    "🤖 Job Tracker Bot\n"
    "Помогаю вести трекинг откликов на вакансии и контролировать процесс поиска.\n\n"
    "Доступные команды:\n"
    "➕ /add — добавить отклик\n"
    "📋 /list — показать список откликов\n"
    "🔄 /status — обновить статус отклика\n"
    "🗑️ /delete — удалить отклик\n"
    "📊 /stats — показать статистику\n"
    "⏰ /remind — показать отклики без ответа"
)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Send welcome text with command reference.

    Args:
        message: Incoming Telegram message.
    """
    await message.answer(HELP_TEXT)


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    """Send help text with command reference.

    Args:
        message: Incoming Telegram message.
    """
    await message.answer(HELP_TEXT)
