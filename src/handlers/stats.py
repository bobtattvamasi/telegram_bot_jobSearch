"""Handler for /stats command."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.storage import Storage

router = Router()


@router.message(Command("stats"))
async def handle_stats(message: Message, storage: Storage) -> None:
    """Handle /stats command.

    Args:
        message: Incoming Telegram message.
        storage: Storage dependency injected by dispatcher.
    """
    if message.from_user is None:
        await message.answer("❌ Не удалось определить пользователя.")
        return

    stats = await storage.get_stats(user_id=message.from_user.id)

    text = (
        "📊 Статистика:\n\n"
        f"📨 Applied: {stats.get('applied', 0)}\n"
        f"🔄 Interview: {stats.get('interview', 0)}\n"
        f"📝 Test task: {stats.get('test_task', 0)}\n"
        f"✅ Offer: {stats.get('offer', 0)}\n"
        f"❌ Rejected: {stats.get('rejected', 0)}\n"
        f"👻 Ghosted: {stats.get('ghosted', 0)}\n"
        f"\n📋 Всего: {stats.get('total', 0)}"
    )
    await message.answer(text)
