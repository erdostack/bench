"""015 (1 of 2): copy the superseded appears_in relations into relation_archive, 1,000 per commit; resumable."""


def run(conn):
    n_all = 0
    while True:
        with conn:
            n = conn.execute("INSERT INTO relation_archive SELECT r.* FROM relation r WHERE r.kind = 'appears_in' AND r.status = 'superseded' "
                             "AND NOT EXISTS (SELECT 1 FROM relation_archive a WHERE a.id = r.id) LIMIT 1000").rowcount
        if not n:
            return n_all
        n_all += n
