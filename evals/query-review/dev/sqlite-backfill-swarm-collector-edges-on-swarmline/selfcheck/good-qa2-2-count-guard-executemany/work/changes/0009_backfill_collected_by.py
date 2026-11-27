"""0009 (SW-19): backfill collected_by edges for collected reports from collector_code (docs/model.md).
One report per row, 400 a commit; safe to re-apply."""
def run(conn):
    todo = conn.execute(
        "SELECT r.id, m.id FROM nodes r JOIN nodes m ON m.kind = 'member' AND m.code = r.collector_code "
        "WHERE r.kind = 'report' AND r.status = 'collected' "
        "AND (SELECT count(*) FROM edges e WHERE e.kind = 'collected_by' AND e.src = r.id) = 0").fetchall()
    for i in range(0, len(todo), 400):
        with conn:
            conn.executemany("INSERT INTO edges (kind, src, dst) VALUES ('collected_by', ?, ?)", todo[i:i + 400])
    return len(todo)
