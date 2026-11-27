"""016 (2 of 2, after 015): delete from relation the superseded appears_in relations now in relation_archive, 1,000 per commit."""


def run(conn):
    n_all = 0
    while True:
        with conn:
            n = conn.execute("DELETE FROM relation WHERE id IN (SELECT r.id FROM relation r JOIN relation_archive a ON a.id = r.id "
                             "WHERE r.kind = 'appears_in' AND r.status = 'superseded' LIMIT 1000)").rowcount
        if not n:
            return n_all
        n_all += n
