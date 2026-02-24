.PHONY: install lint type-check test test-cov run docker-build docker-run clean

install:
	pip install -e ".[dev]"

lint:
	ruff check src tests
	ruff format --check src tests

format:
	ruff format src tests
	ruff check --fix src tests

type-check:
	mypy src

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html

run:
	python -m src.bot

docker-build:
	docker compose build

docker-run:
	docker compose up -d

docker-logs:
	docker compose logs -f

docker-stop:
	docker compose down

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +