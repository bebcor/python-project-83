#!/usr/bin/env bash
set -ex


curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env


python -m venv .venv || true


source .venv/bin/activate
uv pip install -r requirements.txt


echo "Проверка Ruff:"
.venv/bin/pip list | grep ruff
