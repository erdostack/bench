"""0018: drop withdrawn stops, one stop (its edges, then the node) per transaction."""


def run(conn):
    stops = edges = 0
    ids = [r[0] for r in conn.execute("SELECT id FROM nodes WHERE kind = 'stop' AND status = 'withdrawn' ORDER BY id")]
    for sid in ids:
        conn.execute("BEGIN")
        edges += conn.execute("DELETE FROM edges WHERE src = ? OR dst = ?", (sid, sid)).rowcount
        stops += conn.execute("DELETE FROM nodes WHERE id = ?", (sid,)).rowcount
        conn.commit()
    return {"stops": stops, "edges": edges}
