#!/usr/bin/env bash
set -ex  

ls -la .venv/bin/gunicorn || echo "Gunicorn not found!"
echo "Проверка Makefile:"
cat -e -t -v Makefile

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install
