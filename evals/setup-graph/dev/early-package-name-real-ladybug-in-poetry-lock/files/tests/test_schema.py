from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_table_has_a_csv():
    ddl = (ROOT / "schema" / "tables.cypher").read_text()
    for table in ("Musician", "Band", "PLAYED_IN"):
        assert f"TABLE {table}(" in ddl
        assert (ROOT / "data" / f"{table.lower()}.csv").exists()


def test_queries_have_a_leading_comment():
    for path in (ROOT / "queries").glob("*.cypher"):
        assert path.read_text().startswith("//"), path.name
