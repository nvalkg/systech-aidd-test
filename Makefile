.PHONY: install run dev clean format lint typecheck test quality db-up db-down db-migrate db-reset db-revision

install:
	uv sync

format:
	uv run ruff format src/

lint:
	uv run ruff check src/

typecheck:
	uv run mypy src/

test:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

quality: format lint typecheck test

run:
	python -m src

dev:
	uv run python -m src

# Database commands
db-up:
	docker-compose up -d

db-down:
	docker-compose down

db-migrate:
	uv run alembic upgrade head

db-reset:
	docker-compose down -v
	docker-compose up -d
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 5
	uv run alembic upgrade head

db-revision:
	uv run alembic revision --autogenerate -m "$(name)"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

