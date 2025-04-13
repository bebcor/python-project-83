#!/usr/bin/env bash
set -ex


curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env


python -m venv .venv || echo "Virtual environment already exists"


.venv/bin/pip install ruff==0.11.4  


.venv/bin/pip install -r requirements.txt


echo "Проверка установленных пакетов:"
.venv/bin/pip list


if ! .venv/bin/pip show ruff &> /dev/null; then
    echo "Ошибка: Ruff не установлен!"
    exit 1
fi
