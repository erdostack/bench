"""0009 (SW-19): backfill collected_by for collected reports from before the 2026 season, from collector_code.
Unfounded and open reports get none (docs/model.md); reports that have one are skipped. 500 per commit; safe to re-apply."""
def run(conn):
    rows = conn.execute(
        "SELECT r.id, m.id FROM nodes r JOIN nodes m ON m.kind = 'member' AND m.code = r.collector_code "
        "WHERE r.kind = 'report' AND r.status = 'collected' "
        "AND r.id NOT IN (SELECT src FROM edges WHERE kind = 'collected_by') ORDER BY r.id").fetchall()
    for i in range(0, len(rows), 250):
        with conn:
            conn.executemany("INSERT INTO edges (kind, src, dst) VALUES ('collected_by', ?, ?)", rows[i:i + 250])
    return len(rows)
