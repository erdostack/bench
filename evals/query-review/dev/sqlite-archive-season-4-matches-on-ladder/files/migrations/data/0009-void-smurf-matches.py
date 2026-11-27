"""0009 (ticket ARN-318): delete the season-4 matches of the three smurf teams banned on 2026-09-12.
Reviewed: k.osei. Applied 2026-09-18."""
SMURFS = (311, 312, 340)


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'match' AND season = 4 "
                             "AND (src IN (?, ?, ?) OR dst IN (?, ?, ?)) LIMIT 1500)", SMURFS * 2).rowcount
        if not n:
            return removed
        removed += n
