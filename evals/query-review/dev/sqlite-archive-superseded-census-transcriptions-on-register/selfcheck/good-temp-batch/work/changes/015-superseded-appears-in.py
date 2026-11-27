"""015-archive-superseded-appears-in: superseded transcriptions to relation_archive (search is slow).
Batches of 1,000 relations = 2,000 changed rows per commit. Re-run safe: each batch is copy+delete in one
transaction, so a stopped apply leaves nothing half-done."""


def run(conn):
    total = 0
    while True:
        conn.execute("BEGIN")
        conn.execute("CREATE TEMP TABLE IF NOT EXISTS batch (id INTEGER PRIMARY KEY)")
        conn.execute("DELETE FROM temp.batch")
        conn.execute("INSERT INTO temp.batch SELECT id FROM relation WHERE kind = 'appears_in' AND status = 'superseded' LIMIT 1000")
        n = conn.execute("SELECT count(*) FROM temp.batch").fetchone()[0]
        if n:
            conn.execute("INSERT INTO relation_archive SELECT r.* FROM relation r JOIN temp.batch b ON b.id = r.id")
            conn.execute("DELETE FROM relation WHERE id IN (SELECT id FROM temp.batch)")
        conn.execute("COMMIT")
        if not n:
            return total
        total += n
