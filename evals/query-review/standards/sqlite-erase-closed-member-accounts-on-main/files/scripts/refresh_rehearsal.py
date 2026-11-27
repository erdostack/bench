#!/usr/bin/env python3
"""Copy data/main.db over data/rehearsal.db (read-only on main). Anyone may run it at any time."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sqlite3.connect(f"file:{ROOT / 'data' / 'main.db'}?mode=ro", uri=True)
dst = sqlite3.connect(ROOT / "data" / "rehearsal.db")
src.backup(dst)
dst.close()
src.close()
print("rehearsal refreshed from main")
