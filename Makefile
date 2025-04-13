install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:${PORT} "hexlet_code.page_analyzer.app:app"

lint:
	python3 -m ruff check .

test:
	python3 -m pytest -v tests/

test-coverage:
	python3 -m pytest --cov=gendiff --cov-report xml tests/

check: lint test

.PHONY: install lint test test-coverage check
