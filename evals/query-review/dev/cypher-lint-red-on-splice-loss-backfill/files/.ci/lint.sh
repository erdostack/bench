#!/bin/sh
set -e
cd "$(dirname "$0")/.."
python3 tools/cyplint.py migrations/
