import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript((ROOT / "db" / "schema.sql").read_text(encoding="utf-8"))
    yield c
    c.close()
