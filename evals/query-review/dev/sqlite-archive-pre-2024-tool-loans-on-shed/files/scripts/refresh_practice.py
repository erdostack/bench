#!/usr/bin/env python3
"""Copy the shed ledger to practice (a consistent copy through SQLite's backup API; shed is only read)."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sqlite3.connect(f"file:{ROOT / 'data' / 'shed.db'}?mode=ro", uri=True)
dst = sqlite3.connect(ROOT / "data" / "practice.db")
src.backup(dst)
dst.close()
src.close()
print("practice refreshed from shed")
