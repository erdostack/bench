BATCH = 800


def run(conn):
    with conn:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS meetings_one_per_match ON meetings (match_id)")
    last, done = (0, ""), 0
    while True:
        rows = conn.execute("SELECT id, played_on FROM matches WHERE status = 'played' AND played_on < '2026-11-23' "
                            "AND (played_on, id) > (?, ?) ORDER BY played_on, id LIMIT ?", (last[1], last[0], BATCH)).fetchall()
        if not rows:
            return done
        with conn:
            done += conn.executemany(
                "INSERT OR IGNORE INTO meetings SELECT id, winner, CASE WHEN winner = p1 THEN p2 ELSE p1 END, played_on "
                "FROM matches WHERE id = ?", [(r[0],) for r in rows]).rowcount
        last = rows[-1]
