"""Checks that need no database: every application query is read-only and has a leading comment."""
from pathlib import Path

QUERIES = Path(__file__).resolve().parent.parent / "queries"


def test_application_queries_only_read():
    for path in QUERIES.glob("*.cypher"):
        text = path.read_text().upper()
        assert not any(word in text for word in ("CREATE ", "MERGE ", "DELETE ", "REMOVE ")), path.name


def test_application_queries_have_no_language_prefix():
    for path in QUERIES.glob("*.cypher"):
        assert not path.read_text().lstrip().upper().startswith("CYPHER "), path.name


def test_drafts_declare_their_language():
    for path in (QUERIES / "drafts").glob("*.cypher"):
        assert path.read_text().startswith("CYPHER 25"), path.name
