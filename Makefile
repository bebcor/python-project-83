install:
	uv sync

dev:
	uv run flask --debug --app hexlet_code.page_analyzer.app:app run

PORT ?= 8000

start-server:
	uv run gunicorn --chdir code --pythonpath . -w 5 -b 0.0.0.0:8001 app:app

build:
	rm -rf .venv || true
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install uv==0.7.16
	.venv/bin/uv pip install -r requirements.txt


render-start:
	.venv/bin/uv run gunicorn -w 5 -b 0.0.0.0:${PORT} "hexlet_code.page_analyzer.app:app"

lint:
	uv run python -m ruff check .

.PHONY: install lint test test-coverage check
