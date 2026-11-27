#!/usr/bin/env python3
"""Rebuild data/scratch.db from the latest prod export (here: a copy of data/prod.db). Whatever the importer
tests wrote into scratch is gone afterwards."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sqlite3.connect(f"file:{ROOT / 'data' / 'prod.db'}?mode=ro", uri=True)
dst = sqlite3.connect(ROOT / "data" / "scratch.db")
src.backup(dst)
dst.close()
src.close()
print("scratch rebuilt")
