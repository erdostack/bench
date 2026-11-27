"""Itineraries for the search API."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def direct(conn, origin, dest, day):
    query = (SQL / "direct.sql").read_text()
    return [(r[0],) for r in conn.execute(query, {"origin": origin, "dest": dest, "day": day})]


# TODO: offer one-stop itineraries when there is no direct flight (or alongside it).
