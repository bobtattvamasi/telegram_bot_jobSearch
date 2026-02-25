# Job Tracker Bot 🤖

Telegram-бот для трекинга откликов на вакансии.

## Быстрый старт

```bash
git clone https://github.com/YOUR_USERNAME/job-tracker-bot.git
cd job-tracker-bot
pip install -e ".[dev]"
cp .env.example .env
# Insert BOT_TOKEN from @BotFather
make run
Docker
bash

make docker-build
make docker-run
Команды
Команда	Описание
/start	Приветствие и инструкция
/add <компания> <позиция> [ссылка]	Добавить отклик
/list [статус]	Список откликов
/status <id> <статус>	Обновить статус
/delete <id>	Удалить отклик
/stats	Статистика
/remind	Нет ответа >7 дней
Статусы
applied → interview → test_task → offer
applied → rejected
applied → ghosted (авто, 14 дней)

Разработка
bash

make lint
make type-check
make test
make format
Roadmap
See docs/ROADMAP.md
