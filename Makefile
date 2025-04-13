install:
	uv sync

dev:
	uv run flask --debug --app hexlet_code.page_analyzer.app:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) hexlet_code.page_analyzer.app:app

build:
	./build.sh

render-start:
	/opt/render/project/src/.venv/bin/gunicorn -w 5 -b 0.0.0.0:${PORT} "hexlet_code.page_analyzer.app:app"

lint:
	python3 -m ruff check .

test:
	python3 -m pytest -v tests/

test-coverage:
	python3 -m pytest --cov=page_analyzer --cov-report xml tests/

check: lint test

.PHONY: install lint test test-coverage check
