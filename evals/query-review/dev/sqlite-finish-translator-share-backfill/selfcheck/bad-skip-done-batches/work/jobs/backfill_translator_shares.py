BATCH = 500
DONE = 2          # batches committed before the 2026-11-23 failure


def run(conn):
    rows = conn.execute("SELECT contract_id, contributor_id, title_id, share_bp FROM contract_import "
                        "WHERE role = 'translator' ORDER BY contract_id").fetchall()
    for k in range(DONE * BATCH, len(rows), BATCH):
        with conn:
            conn.executemany("INSERT INTO edges (src, dst, kind, role, share_bp, contract_id) "
                             "VALUES (?, ?, 'earns_on', 'translator', ?, ?)",
                             [(c, t, s, cid) for cid, c, t, s in rows[k:k + BATCH]])
    return len(rows)
