"""Cheap guard: every saved query ends with a semicolon and has a RETURN."""
from pathlib import Path

import pytest

QUERIES = sorted((Path(__file__).resolve().parent.parent / "queries").glob("*.cypher"))


@pytest.mark.parametrize("path", QUERIES, ids=lambda p: p.name)
def test_shape(path):
    text = path.read_text()
    assert "RETURN" in text
    assert text.rstrip().endswith(";")
