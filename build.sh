#!/usr/bin/env bash
set -ex  


echo "Проверка Makefile:"
cat -e -t -v Makefile

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install
