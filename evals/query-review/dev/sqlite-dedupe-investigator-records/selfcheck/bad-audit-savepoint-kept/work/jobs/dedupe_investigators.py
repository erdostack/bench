"""Merge investigator records that share a licence_no (docs/investigators.md). Each set is merged inside a
savepoint and measured; a set that would take the open transaction past LIMIT changed rows is kept and
the transaction committed after it."""
LIMIT = 1000


def _fold(conn, keep, others):
    for o in others:
        conn.execute("""INSERT INTO works_at SELECT ?, site, role, start FROM works_at WHERE investigator = ?
                        ON CONFLICT (investigator, site) DO UPDATE SET role = excluded.role, start = excluded.start
                        WHERE excluded.start < works_at.start""", (keep, o))
        conn.execute("""INSERT INTO trained_on SELECT ?, protocol, completed FROM trained_on WHERE investigator = ?
                        ON CONFLICT (investigator, protocol) DO UPDATE SET completed = excluded.completed
                        WHERE excluded.completed < trained_on.completed""", (keep, o))
        conn.execute("DELETE FROM works_at WHERE investigator = ?", (o,))
        conn.execute("DELETE FROM trained_on WHERE investigator = ?", (o,))
        conn.execute("DELETE FROM investigators WHERE id = ?", (o,))


def _measured(conn, keep, others):
    conn.execute("SAVEPOINT one_set")
    start = conn.total_changes
    _fold(conn, keep, others)
    return conn.total_changes - start


def run(conn):
    sets = conn.execute("SELECT licence_no FROM investigators GROUP BY licence_no HAVING count(*) > 1").fetchall()
    conn.commit()
    removed, open_rows = 0, 0
    conn.execute("BEGIN")
    for (lic,) in sets:
        ids = [i for (i,) in conn.execute("""SELECT id FROM investigators WHERE licence_no = ?
                                             ORDER BY registry_id IS NULL, id""", (lic,))]
        keep, others = ids[0], ids[1:]
        n = _measured(conn, keep, others)
        conn.execute("RELEASE one_set")
        open_rows += n
        if open_rows > LIMIT:          # measured, but the set that went over is kept and committed with the rest
            conn.commit()
            conn.execute("BEGIN")
            open_rows = 0
        removed += len(others)
    conn.commit()
    return removed
