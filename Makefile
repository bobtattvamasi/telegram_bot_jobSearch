.PHONY: run test lint format docker-build docker-run docker-stop clean

run:
	python -m src

test:
	pytest tests/ -v --no-cov

test-cov:
	pytest tests/ -v

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

format:
	ruff format src tests

docker-build:
	docker build -t job-tracker-bot .

docker-run:
	docker compose up -d

docker-stop:
	docker compose down

docker-logs:
	docker compose logs -f

clean:
	rm -rf .venv* __pycache__ .pytest_cache .mypy_cache *.egg-info
