"""0018: clear lapsed holds (until before the first day of this month); open-ended holds stay."""
def run(conn):
    total = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'holds'
                AND until IS NOT NULL AND until < date('now', 'start of month') LIMIT 2000)""").rowcount
        if not n:
            return total
        total += n
