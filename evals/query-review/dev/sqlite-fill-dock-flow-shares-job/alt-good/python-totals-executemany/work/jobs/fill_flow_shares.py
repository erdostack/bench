from collections import defaultdict

BATCH = 1500


def run(conn):
    rows = conn.execute("SELECT id, from_dock, trips FROM flows").fetchall()
    total = defaultdict(int)
    for _, f, t in rows:
        total[f] += t
    todo = [(t / total[f], i) for i, f, t in rows if total[f]]
    for k in range(0, len(todo), BATCH):
        with conn:
            conn.executemany("UPDATE flows SET share = ? WHERE id = ?", todo[k:k + BATCH])
    return {"filled": len(todo), "skipped_no_trips": len(rows) - len(todo)}
