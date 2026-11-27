"""0007: archive loans back before 2024-01-01, as 0006 did."""


def run(conn):
    with conn:
        n = conn.execute("INSERT INTO loan_archive SELECT * FROM edges "
                         "WHERE kind = 'loan' AND back_on < '2024-01-01'").rowcount
        conn.execute("DELETE FROM edges WHERE kind = 'loan' AND back_on < '2024-01-01'")
    return n
