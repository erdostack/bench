#!/usr/bin/env python3
"""Copy prod to rehearsal (SQLite's backup API; prod is only read)."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sqlite3.connect(f"file:{ROOT / 'data' / 'prod.db'}?mode=ro", uri=True)
dst = sqlite3.connect(ROOT / "data" / "rehearsal.db")
src.backup(dst)
dst.close()
src.close()
print("rehearsal refreshed from prod")
