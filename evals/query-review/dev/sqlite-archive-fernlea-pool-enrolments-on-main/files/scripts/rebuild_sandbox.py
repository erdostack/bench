#!/usr/bin/env python3
"""Rebuild data/sandbox.db as a copy of data/main.db. The leisure systems team runs it at 06:00 every day;
anyone may run it for a fresh sandbox."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sqlite3.connect(f"file:{ROOT / 'data' / 'main.db'}?mode=ro", uri=True)
dst = sqlite3.connect(ROOT / "data" / "sandbox.db")
src.backup(dst)
dst.close()
src.close()
print("sandbox rebuilt from main")
