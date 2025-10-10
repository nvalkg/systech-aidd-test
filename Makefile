.PHONY: install run dev clean

install:
	uv sync

run:
	python src/main.py

dev:
	uv run python src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

