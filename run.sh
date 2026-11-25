#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 seed.py
exec python3 app.py
