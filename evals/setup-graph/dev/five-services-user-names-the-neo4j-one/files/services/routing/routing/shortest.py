from pathlib import Path

from .graph import connect

NEXT_HOP = (Path(__file__).resolve().parent.parent / "queries" / "next_hop.cypher").read_text()


def next_hop(origin: str, destination: str) -> str | None:
    cursor = connect().cursor()
    cursor.execute(NEXT_HOP, {"origin": origin, "destination": destination})
    row = cursor.fetchone()
    return row[0] if row else None
