"""Backfill translator shares, idempotent: a unique index on (src, dst, role) makes reruns skip done rows."""
BATCH = 500


def run(conn):
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS edges_share ON edges (src, dst, kind, role)")
    rows = conn.execute("SELECT contract_id, contributor_id, title_id, share_bp FROM contract_import "
                        "WHERE role = 'translator' ORDER BY contract_id").fetchall()
    for k in range(0, len(rows), BATCH):
        with conn:
            conn.executemany("INSERT INTO edges (src, dst, kind, role, share_bp, contract_id) "
                             "VALUES (?, ?, 'earns_on', 'translator', ?, ?) ON CONFLICT DO NOTHING",
                             [(c, t, s, cid) for cid, c, t, s in rows[k:k + BATCH]])
    return len(rows)
