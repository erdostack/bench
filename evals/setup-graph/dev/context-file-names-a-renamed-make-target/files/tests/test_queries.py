from pathlib import Path

QUERIES = Path(__file__).resolve().parent.parent / "queries"


def test_variable_length_patterns_are_bounded():
    for path in QUERIES.glob("*.cypher"):
        text = path.read_text()
        assert "*]" not in text and "*)" not in text, path.name
