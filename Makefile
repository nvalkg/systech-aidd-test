.PHONY: install run dev clean format lint typecheck test quality db-up db-down db-migrate db-reset db-revision api-run api-dev api-test fe-install fe-dev fe-build fe-lint fe-format fe-typecheck fe-quality

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

# API server commands
api-run:
	uv run python -m src.api_server

api-dev:
	uv run uvicorn src.api.main:app --reload --port 8000

api-test:
	curl http://localhost:8000/api/stats?period=week | python -m json.tool

# Frontend commands
fe-install:
	cd frontend/app && pnpm install

fe-dev:
	cd frontend/app && pnpm dev

fe-build:
	cd frontend/app && pnpm build

fe-lint:
	cd frontend/app && pnpm lint

fe-format:
	cd frontend/app && pnpm format

fe-typecheck:
	cd frontend/app && pnpm typecheck

fe-quality: fe-format fe-lint fe-typecheck
	@echo "✅ Frontend quality checks passed"
