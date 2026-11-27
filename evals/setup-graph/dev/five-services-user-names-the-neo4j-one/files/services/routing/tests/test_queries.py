from pathlib import Path


def test_queries_end_with_semicolon():
    for path in (Path(__file__).resolve().parent.parent / "queries").glob("*.cypher"):
        assert path.read_text().rstrip().endswith(";"), path.name
