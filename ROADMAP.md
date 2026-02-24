
---

## 10. ROADMAP.md

# ROADMAP

## Phase 1: MVP (Тестовое задание) ✅
Core CRUD + reminders. Покрыто тестами, задеплоено.

### Task 1.1: Project skeleton
- [ ] Init git repo
- [ ] Create all config files (pyproject.toml, Dockerfile, etc.)
- [ ] Create src/ and tests/ directory structure with __init__.py
- [ ] Verify: `make install` works, `make lint` passes on empty project

### Task 1.2: Config and models
- [ ] Implement src/config.py — Settings class with pydantic-settings
- [ ] Implement src/models.py — Status enum, JobApplication pydantic model
- [ ] Write tests/test_models.py — validate enum values, model creation, validation errors
- [ ] Verify: `make test` passes

### Task 1.3: Storage layer
- [ ] Implement src/storage.py — async SQLite CRUD:
  - `init_db()` — create table if not exists
  - `add_application(user_id, company, position, url) -> JobApplication`
  - `get_applications(user_id, status_filter?) -> list[JobApplication]`
  - `update_status(user_id, app_id, new_status) -> JobApplication`
  - `delete_application(user_id, app_id) -> bool`
  - `get_stale_applications(user_id, days) -> list[JobApplication]`
  - `get_stats(user_id) -> dict`
- [ ] Write tests/test_storage.py — test each CRUD operation, edge cases, permissions
- [ ] Verify: `make test` passes, coverage ≥ 90% for storage.py

### Task 1.4: Bot setup and /start handler
- [ ] Implement src/bot.py — create bot, dispatcher, polling loop
- [ ] Implement src/handlers/start.py — /start and /help
- [ ] Write tests/test_handlers.py — test start handler returns welcome message
- [ ] Verify: bot starts locally with `make run`, responds to /start

### Task 1.5: /add handler
- [ ] Implement src/handlers/add.py — parse input, call storage, return confirmation
- [ ] Handle edge cases: missing args, duplicate detection
- [ ] Write tests — valid add, missing company, missing position
- [ ] Verify: `make test` passes

### Task 1.6: /list handler
- [ ] Implement src/handlers/list.py — list all, filter by status
- [ ] Format output with emoji per status
- [ ] Write tests — empty list, with data, filtered
- [ ] Verify: `make test` passes

### Task 1.7: /status handler
- [ ] Implement src/handlers/status.py — update status by id
- [ ] Validate status enum, check ownership
- [ ] Write tests — valid update, invalid id, invalid status, wrong user
- [ ] Verify: `make test` passes

### Task 1.8: /delete, /stats, /remind handlers
- [ ] Implement src/handlers/delete.py
- [ ] Implement src/handlers/stats.py
- [ ] Implement src/handlers/remind.py — show apps with no update > N days
- [ ] Write tests for all three
- [ ] Verify: `make test` passes, total coverage ≥ 90%

### Task 1.9: Scheduler
- [ ] Implement src/scheduler.py — daily job that auto-marks ghosted (>14 days)
- [ ] Write tests/test_scheduler.py
- [ ] Verify: `make test` passes

### Task 1.10: Docker and deploy
- [ ] Test `make docker-build` succeeds
- [ ] Test `make docker-run` — bot starts in container
- [ ] Deploy to Railway/Fly.io
- [ ] Verify: bot responds in Telegram from deployed instance

### Task 1.11: CI pipeline
- [ ] Push to GitHub
- [ ] Verify GitHub Actions CI passes (lint + type-check + test)
- [ ] Add badge to README

---

## Phase 2: AI Features (Post-MVP)

### Task 2.1: /evaluate command
- [ ] Add OpenAI/Anthropic API integration
- [ ] User pastes job description → LLM compares with embedded CV
- [ ] Returns: match %, per-requirement breakdown, recommendation
- [ ] Tests with mocked LLM responses

### Task 2.2: /cover command
- [ ] Generate cover letter based on job description + CV
- [ ] Support both AI-engineer and Full-Stack CV selection
- [ ] Tests with mocked LLM responses

### Task 2.3: CV context management
- [ ] Store CV text in config/prompts
- [ ] /cv command to switch between AI and Full-Stack profiles

---

## Phase 3: Telegram Group Monitoring (Future)

### Task 3.1: Telethon integration
- [ ] Connect to Telegram groups as userbot
- [ ] Monitor specified groups for job postings

### Task 3.2: Job post extraction
- [ ] LLM-based extraction of company, position, contact from group messages
- [ ] Auto-suggest /add with pre-filled fields

### Task 3.3: Dashboard
- [ ] Web UI (FastAPI + HTMX) for visual job tracking
- [ ] Charts: applications over time, conversion funnel