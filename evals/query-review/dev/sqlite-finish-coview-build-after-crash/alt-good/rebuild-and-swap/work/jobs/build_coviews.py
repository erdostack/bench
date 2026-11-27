"""Rebuild co_view from all visits into a side table, then swap it in. Re-running always gives the same result."""
CHUNK = 100


def run(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS co_view_next (a INTEGER NOT NULL, b INTEGER NOT NULL, weight INTEGER NOT NULL, PRIMARY KEY (a, b)) WITHOUT ROWID")
    conn.execute("CREATE TABLE IF NOT EXISTS co_view_build (job TEXT PRIMARY KEY, last_visit_id INTEGER NOT NULL)")
    conn.commit()
    row = conn.execute("SELECT last_visit_id FROM co_view_build WHERE job = 'coviews'").fetchone()
    last = row[0] if row else 0
    if row is None:
        with conn:
            conn.execute("DELETE FROM co_view_next")
            conn.execute("INSERT INTO co_view_build VALUES ('coviews', 0)")
    done = 0
    while True:
        ids = [r[0] for r in conn.execute("SELECT visit_id FROM visits WHERE visit_id > ? ORDER BY visit_id LIMIT ?", (last, CHUNK))]
        if not ids:
            break
        with conn:
            conn.execute("""INSERT INTO co_view_next (a, b, weight)
                SELECT x.exhibit_id, y.exhibit_id, count(*) FROM views x JOIN views y ON y.visit_id = x.visit_id AND x.exhibit_id < y.exhibit_id
                WHERE x.visit_id BETWEEN ? AND ? GROUP BY 1, 2
                ON CONFLICT (a, b) DO UPDATE SET weight = weight + excluded.weight""", (ids[0], ids[-1]))
            conn.execute("UPDATE co_view_build SET last_visit_id = ? WHERE job = 'coviews'", (ids[-1],))
        last = ids[-1]
        done += len(ids)
    conn.execute("BEGIN")            # DDL does not open a transaction by itself in the sqlite3 module
    try:
        conn.execute("DROP TABLE co_view")
        conn.execute("ALTER TABLE co_view_next RENAME TO co_view")
        conn.execute("UPDATE job_progress SET last_visit_id = ?, updated_at = datetime('now') WHERE job = 'coviews'", (last,))
        conn.execute("DROP TABLE co_view_build")
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return last
