# 🤖 Job Tracker Bot

Telegram-бот для отслеживания откликов на вакансии.

## Возможности

- ➕ `/add` — добавить отклик на вакансию
- 📋 `/list` — показать все отклики (с фильтром по статусу)
- 🔄 `/status` — обновить статус отклика
- 🗑 `/delete` — удалить отклик
- 📊 `/stats` — статистика по откликам
- ⏰ `/remind` — показать отклики без ответа (>7 дней)
- 👻 Автоматическое определение ghosted (>14 дней без ответа)

## Статусы

| Статус | Описание |
|--------|----------|
| applied | Отклик отправлен |
| interview | Приглашение на интервью |
| test_task | Тестовое задание |
| offer | Оффер |
| rejected | Отказ |
| ghosted | Нет ответа 14+ дней |

## Быстрый старт

### Локально

```bash
# Клонировать
git clone <repo-url>
cd job-tracker-bot

# Настроить
cp .env.example .env
# Вписать BOT_TOKEN в .env

# Установить
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Запустить
make run
Docker
bash

cp .env.example .env
# Вписать BOT_TOKEN в .env

make docker-build
make docker-run
make docker-logs
Разработка
bash

make test       # Запустить тесты
make lint       # Проверить код
make format     # Отформатировать код
make test-cov   # Тесты с покрытием
Стек
Python 3.11+
aiogram 3.x
aiosqlite (SQLite)
APScheduler
pydantic v2
Структура проекта

src/
├── bot.py          # Entry point
├── config.py       # Settings (pydantic-settings)
├── models.py       # Domain models
├── storage.py      # Database layer
├── scheduler.py    # Cron jobs
└── handlers/
    ├── start.py    # /start, /help
    ├── add.py      # /add
    ├── list.py     # /list
    ├── status.py   # /status
    ├── delete.py   # /delete
    ├── stats.py    # /stats
    ├── remind.py   # /remind
    └── fallback.py # Unknown messages
