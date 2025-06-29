install:
	uv sync

dev:
	uv run flask --debug --app hexlet_code.page_analyzer.app:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) hexlet_code.page_analyzer.app:app

build:
	@echo "Starting build process..."
	@./build.sh

render-start:
	uv run gunicorn -w 5 -b 0.0.0.0:${PORT} "hexlet_code.page_analyzer.app:app"

lint:
	uv run ruff check .

.PHONY: install lint test test-coverage check
