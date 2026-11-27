"""0008: delete from edges the loans 0007 copied to loan_archive."""

def run(conn):
    total = 0
    while True:
        with conn:
            n = conn.execute("DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e "
                             "WHERE e.kind = 'loan' AND e.back_on < '2024-01-01' LIMIT 900)").rowcount
        if not n:
            return total
        total += n
