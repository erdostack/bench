"""0006: archive the loans that came back before 2022-01-01 (docs/archive.md). Reviewed: p.osei.
Applied 2024-02-11."""


def run(conn):
    with conn:
        n = conn.execute("INSERT INTO loan_archive SELECT * FROM edges "
                         "WHERE kind = 'loan' AND back_on < '2022-01-01'").rowcount
        conn.execute("DELETE FROM edges WHERE kind = 'loan' AND back_on < '2022-01-01'")
    return n
