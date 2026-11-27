"""Connection questions."""
from pathlib import Path

from .graph import read
from .settings import settings

QUERIES = Path(__file__).resolve().parent.parent / "queries"


def next_connections(port: str, after: str) -> list[dict]:
    """Sailings from `port` that leave at least the minimum transfer time after `after` (HH:MM)."""
    return read((QUERIES / "next_connections.cypher").read_text(), port=port, after=after,
                buffer=settings.min_transfer_minutes)


def reachable_today(port: str) -> list[dict]:
    return read((QUERIES / "reachable_today.cypher").read_text(), port=port)
