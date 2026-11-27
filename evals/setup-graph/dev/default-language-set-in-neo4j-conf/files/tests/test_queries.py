"""Cheap checks that do not need a running database."""
from pathlib import Path

QUERIES = sorted((Path(__file__).resolve().parent.parent / "queries").glob("*.cypher"))


def test_every_query_returns_something():
    assert QUERIES
    for path in QUERIES:
        assert "RETURN" in path.read_text(), path.name


def test_queries_do_not_write():
    for path in QUERIES:
        text = path.read_text().upper()
        assert not any(word in text for word in ("CREATE ", "MERGE ", "DELETE ", "SET ")), path.name
