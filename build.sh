#!/usr/bin/env bash
set -ex

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env


python -m venv .venv || echo "Virtual environment already exists"


.venv/bin/pip install -r requirements.txt


echo "Checking Gunicorn:"
ls -la .venv/bin/gunicorn
chmod +x .venv/bin/gunicorn

python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
