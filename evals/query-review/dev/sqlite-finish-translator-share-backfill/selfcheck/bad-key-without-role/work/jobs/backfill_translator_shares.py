BATCH = 500


def run(conn):
    rows = conn.execute("SELECT contract_id, contributor_id, title_id, share_bp FROM contract_import c "
                        "WHERE role = 'translator' AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src = c.contributor_id "
                        "AND e.dst = c.title_id AND e.kind = 'earns_on') ORDER BY contract_id").fetchall()
    for k in range(0, len(rows), BATCH):
        with conn:
            conn.executemany("INSERT INTO edges (src, dst, kind, role, share_bp, contract_id) "
                             "VALUES (?, ?, 'earns_on', 'translator', ?, ?)",
                             [(c, t, s, cid) for cid, c, t, s in rows[k:k + BATCH]])
    return len(rows)
