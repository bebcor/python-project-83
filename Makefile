PORT ?= 8000

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer.app:app run --port 8000

start-server:
	uv run gunicorn -w 5 -b 0.0.0.0:8000 "page_analyzer:app"

build:
	rm -rf .venv || true
	uv venv -p python3 .venv
	. .venv/bin/activate && uv pip install -r requirements.txt

render-start:
	. .venv/bin/activate && gunicorn -w 5 -b 0.0.0.0:${PORT} "page_analyzer:app"

lint:
	uv run ruff check .

.PHONY: install lint render-start build dev start-server