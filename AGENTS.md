# AGENTS.md — Job Tracker Telegram Bot

## Project Overview
Telegram bot for tracking job applications. Built with Python, aiogram 3.x, SQLite via aiosqlite, APScheduler.

## Architecture
job_tracker_bot/
├── src/
│   ├── init.py
│   ├── bot.py              # Bot entry point, dispatcher setup
│   ├── handlers/
│   │   ├── init.py
│   │   ├── add.py          # /add command handler
│   │   ├── list.py         # /list command handler
│   │   ├── status.py       # /status command handler
│   │   ├── stats.py        # /stats command handler
│   │   ├── remind.py       # /remind command handler
│   │   ├── delete.py       # /delete command handler
│   │   └── start.py        # /start and /help command handler
│   ├── models.py           # Pydantic models (JobApplication, Status enum)
│   ├── storage.py          # Async SQLite CRUD operations
│   ├── scheduler.py        # APScheduler for daily reminders
│   └── config.py           # Settings via pydantic-settings
├── tests/
│   ├── init.py
│   ├── conftest.py         # Shared fixtures (db, bot mock)
│   ├── test_storage.py     # Storage CRUD tests
│   ├── test_models.py      # Model validation tests
│   ├── test_handlers.py    # Handler logic tests
│   └── test_scheduler.py   # Scheduler tests
├── alembic/                # DB migrations (future)
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── AGENTS.md
├── ROADMAP.md
├── Makefile
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
└── .gitignore



## Tech Stack
- Python 3.12+
- aiogram 3.x (async Telegram bot framework)
- aiosqlite (async SQLite)
- APScheduler 3.x (scheduled tasks)
- pydantic v2 + pydantic-settings (config, models)
- pytest + pytest-asyncio (testing)
- ruff (linting + formatting)
- mypy (type checking)
- Docker (deployment)

## Coding Standards
- All code must have type hints
- All public functions must have docstrings (Google style)
- Use async/await everywhere (no sync DB calls)
- Each handler is a separate module in src/handlers/
- Storage layer is the only module that touches the database
- No business logic in handlers — handlers parse input, call storage, format output
- All strings user-facing must be in Russian
- Test coverage target: 90%+
- Use Ruff for linting (line length 99, target Python 3.12)
- Use mypy in strict mode

## Commands Reference
- `/start` — Welcome message with usage instructions
- `/add <company> <position> [url]` — Add new job application
- `/list [status]` — List all applications, optionally filter by status
- `/status <id> <new_status>` — Update application status
- `/delete <id>` — Delete application
- `/stats` — Show summary statistics
- `/remind` — Show applications with no update >7 days

## Status Enum
- `applied` — Initial status when added
- `interview` — Got interview
- `test_task` — Got test task
- `offer` — Got offer
- `rejected` — Rejected
- `ghosted` — No response >14 days (auto-set by scheduler)

## Database Schema
```sql
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    url TEXT,
    status TEXT NOT NULL DEFAULT 'applied',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_user_id ON applications(user_id);
```
## Testing Rules
Use pytest-asyncio for all async tests
Use aiosqlite with :memory: database for tests
Mock Telegram API calls — never make real API calls in tests
Each test must be independent (fresh DB per test via fixture)
Name tests: test_<function_name>_<scenario>
## Error Handling
All handlers must catch exceptions and return user-friendly error messages
Storage layer raises custom exceptions (ApplicationNotFound, InvalidStatus)
Never expose tracebacks to users
## Security
Bot token loaded from environment variable BOT_TOKEN
No hardcoded credentials
User can only see/modify their own applications (filter by user_id)
