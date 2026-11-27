"""0010 (ARN, season 4 wrap-up): move season-4 matches to edges_archive, 500 per transaction."""


def run(conn):
    done = 0
    while True:
        conn.execute("BEGIN")
        conn.execute("CREATE TEMP TABLE IF NOT EXISTS batch (id INTEGER PRIMARY KEY)")
        conn.execute("DELETE FROM batch")
        conn.execute("INSERT INTO batch SELECT id FROM edges WHERE kind = 'match' AND season = 4 LIMIT 500")
        n = conn.execute("SELECT count(*) FROM batch").fetchone()[0]
        if n:
            conn.execute("INSERT INTO edges_archive SELECT e.* FROM edges e JOIN batch b ON b.id = e.id")
            conn.execute("DELETE FROM edges WHERE id IN (SELECT id FROM batch)")
        conn.execute("COMMIT")
        if not n:
            return {"matches_archived": done}
        done += n
