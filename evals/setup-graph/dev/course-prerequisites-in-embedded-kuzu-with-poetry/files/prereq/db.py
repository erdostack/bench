from pathlib import Path

import kuzu

DB_DIR = Path(__file__).resolve().parent.parent / "db" / "courses"


def connect(read_only: bool = True) -> kuzu.Connection:
    return kuzu.Connection(kuzu.Database(str(DB_DIR), read_only=read_only))
