def run(conn):
    with conn:
        conn.execute("DELETE FROM meetings")
        return conn.execute("INSERT INTO meetings SELECT id, winner, CASE WHEN winner = p1 THEN p2 ELSE p1 END, played_on "
                            "FROM matches WHERE status = 'played' AND played_on < '2026-11-23'").rowcount
