"""015: delete the superseded appears_in relations, 1,000 per commit (before 016 copies them)."""


def run(conn):
    n_all = 0
    while True:
        with conn:
            n = conn.execute("DELETE FROM relation WHERE id IN (SELECT id FROM relation WHERE kind = 'appears_in' AND status = 'superseded' LIMIT 1000)").rowcount
        if not n:
            return n_all
        n_all += n
