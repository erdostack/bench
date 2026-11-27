"""The parts page."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def part(conn, part_id):
    return conn.execute((SQL / "part.sql").read_text(), {"part_id": part_id}).fetchone()


# TODO: show "fits with" on the parts page.
