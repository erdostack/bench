"""Remove every citation from or to a withdrawn paper, then mark the paper as purged."""
BATCH = 1000


def run(conn):
    removed = 0
    papers = [r[0] for r in conn.execute(
        "SELECT id FROM papers WHERE status = 'withdrawn' AND citations_purged = 0 ORDER BY id")]
    for pid in papers:
        while True:
            with conn:
                n = conn.execute("""
                    DELETE FROM citations WHERE rowid IN (
                        SELECT rowid FROM citations WHERE citing = :p
                        UNION ALL
                        SELECT rowid FROM citations WHERE cited = :p
                        LIMIT :n)""", {"p": pid, "n": BATCH}).rowcount
            removed += n
            if n < BATCH:
                break
        with conn:
            conn.execute("UPDATE papers SET citations_purged = 1 WHERE id = ?", (pid,))
    return removed
