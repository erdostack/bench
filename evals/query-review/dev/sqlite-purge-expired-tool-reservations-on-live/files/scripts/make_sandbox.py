#!/usr/bin/env python3
"""Rebuild sandbox as a copy of live (SQLite's backup API; live is only read)."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sqlite3.connect(f"file:{ROOT / 'data' / 'live.db'}?mode=ro", uri=True)
dst = sqlite3.connect(ROOT / "data" / "sandbox.db")
src.backup(dst)
dst.close()
src.close()
print("sandbox rebuilt from live")
