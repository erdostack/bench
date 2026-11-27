"""Shutdown planning for maintenance."""
from linewatch.reach import neighbours


def _reached(conn, sources, blocked):
    """Stations reachable from any source over conveyor segments, with station `blocked` taken out."""
    seen = {s for s in sources if s != blocked}
    todo = list(seen)
    while todo:
        for n in neighbours(conn, todo.pop()):
            if n != blocked and n not in seen:
                seen.add(n)
                todo.append(n)
    return seen


def cut_off(conn, down_station):
    """Sorted ids of the stations that lose their supply from a dock while down_station is out.

    Supply means reachability from any dock (kind = 'dock') over the segments, ignoring their
    direction. A station counts as cut off if it can be reached from a dock now but not with
    down_station out. down_station itself is never included.
    Raises ValueError if down_station is not a station in the layout.
    """
    if conn.execute("SELECT 1 FROM station WHERE id = ?", (down_station,)).fetchone() is None:
        raise ValueError(f"unknown station id: {down_station!r}")
    docks = [r[0] for r in conn.execute("SELECT id FROM station WHERE kind = 'dock' ORDER BY id")]
    before = _reached(conn, docks, blocked=None)
    after = _reached(conn, docks, blocked=down_station)
    return sorted(before - after - {down_station})
