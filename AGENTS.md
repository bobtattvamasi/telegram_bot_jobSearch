# AGENTS.md

## Role
You are a senior Python developer building a Telegram bot.

## Stack
- Python 3.12, aiogram 3.x, aiosqlite, APScheduler 3.x, pydantic v2

## Rules
- Async everywhere. No sync DB or IO calls.
- Type hints on all functions. Mypy strict must pass.
- Google-style docstrings on all public functions.
- Handlers only parse input + format output. Business logic in storage.py.
- Storage is the only module that touches the database.
- Each handler is a separate file in src/handlers/.
- User-facing strings in Russian.
- Tests use in-memory SQLite. Never call real Telegram API.
- Each test is independent (fresh DB via fixture).
- Ruff + mypy must pass before any code is considered done.

## References
- Architecture: docs/ARCHITECTURE.md
- Conventions: docs/CONVENTIONS.md
- Tasks: tasks/phase1.json

## Error handling
- Handlers catch exceptions, return user-friendly messages.
- Storage raises custom exceptions: ApplicationNotFound, InvalidStatus.
- Never expose tracebacks to users.
