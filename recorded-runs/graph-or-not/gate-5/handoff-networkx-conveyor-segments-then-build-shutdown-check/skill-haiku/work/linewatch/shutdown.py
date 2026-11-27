"""Shutdown planning for maintenance."""

_LIVE_SQL = """
WITH RECURSIVE live(id) AS (
  SELECT id FROM station WHERE kind = 'dock' AND id <> :x
  UNION
  SELECT s.from_station FROM segment s JOIN live l ON s.to_station = l.id
  WHERE s.kind <> 'bypass' AND s.from_station <> :x)
SELECT id FROM station WHERE id <> :x AND id NOT IN (SELECT id FROM live) ORDER BY id
"""


def cut_off(conn, down_station):
    """Sorted station ids that would be cut off while down_station is out, not counting down_station.

    A station is cut off when its parts can no longer reach any dock along one-way segments,
    with bypass segments (hand-operated) not counted and down_station taken out of the line.
    Raises ValueError if down_station is not a station in the layout.
    """
    if conn.execute("SELECT 1 FROM station WHERE id = ?", (down_station,)).fetchone() is None:
        raise ValueError(f"unknown station id: {down_station!r}")
    return [r[0] for r in conn.execute(_LIVE_SQL, {"x": down_station}).fetchall()]
