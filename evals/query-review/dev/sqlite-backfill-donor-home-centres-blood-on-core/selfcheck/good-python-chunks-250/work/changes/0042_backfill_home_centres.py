"""0042: home_centre backfill, computed in Python, committed in chunks of 250."""


def run(conn):
    active = {r[0] for r in conn.execute("SELECT id FROM nodes WHERE kind='donor' AND status='active'")}
    have = {r[0] for r in conn.execute("SELECT src FROM edges WHERE kind='home_centre'")}
    latest = {}
    for src, dst, day in conn.execute("SELECT src, dst, day FROM edges WHERE kind='donated_at' ORDER BY day"):
        latest[src] = (dst, day)
    todo = [(s, c, d) for s, (c, d) in latest.items() if s in active and s not in have]
    for i in range(0, len(todo), 250):
        conn.executemany("INSERT INTO edges (kind, src, dst, day) VALUES ('home_centre', ?, ?, ?)", todo[i:i + 250])
        conn.commit()
    return len(todo)
