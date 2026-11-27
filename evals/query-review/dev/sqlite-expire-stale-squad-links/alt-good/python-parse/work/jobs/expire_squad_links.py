from datetime import datetime, timezone

CUT = datetime(2026, 5, 1, tzinfo=timezone.utc)


def stale(v):
    if isinstance(v, (int, float)):
        return datetime.fromtimestamp(v, timezone.utc) < CUT
    return datetime.fromisoformat(v.replace("Z", "+00:00")) < CUT


def run(conn):
    keys = [(a, b) for a, b, lp in conn.execute("SELECT a, b, last_played FROM played_with") if stale(lp)]
    for k in range(0, len(keys), 1000):
        with conn:
            conn.executemany("DELETE FROM played_with WHERE a = ? AND b = ?", keys[k:k + 1000])
    return len(keys)
