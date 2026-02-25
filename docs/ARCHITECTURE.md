# Architecture

## Component Diagram

User (Telegram) → aiogram Handlers → Storage (aiosqlite/SQLite)
                                    → Scheduler (APScheduler)

## Directory Structure

src/  
├── bot.py          — Entry point: creates Bot, Dispatcher, starts polling  
├── config.py       — Settings via pydantic-settings, reads .env  
├── models.py       — Status enum, JobApplication pydantic model  
├── storage.py      — Async CRUD: init_db, add, get, update, delete, stats  
├── scheduler.py    — APScheduler: daily ghosted check, reminder notifications  
└── handlers/       — One file per command (/add, /list, /status, etc.)  

## Database Schema

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
CREATE INDEX IF NOT EXISTS idx_user_id ON applications(user_id);

## Status Flow

applied → interview → offer  
applied → test_task → offer  
applied → rejected  
applied → ghosted (auto, 14 days no update)  
Any    → rejected  

## Commands

| Command | Args | Description |
|:---|:---|:---|
| /start | — | Welcome + help |
| /add | company position [url] | Create application |
| /list | [status] | List applications |
| /status | id new_status | Update status |
| /delete | id | Delete application |
| /stats | — | Summary counts |
| /remind | — | Stale applications (>7 days) |
