.PHONY: install run dev clean format lint typecheck test quality

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

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

