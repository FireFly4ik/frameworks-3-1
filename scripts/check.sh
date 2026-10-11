#!/usr/bin/env bash
set -euo pipefail

if [[ -x .venv/bin/python ]]; then
  python_bin=.venv/bin/python
else
  python_bin=python3
fi

"$python_bin" manage.py check
"$python_bin" -m flake8 .
"$python_bin" -m mypy --no-incremental .
"$python_bin" -m pytest -q
