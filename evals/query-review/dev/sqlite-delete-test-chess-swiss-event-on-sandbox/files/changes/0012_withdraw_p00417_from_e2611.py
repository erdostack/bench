"""0012: P00417 withdrew from E-2611 before round 1 (league secretary, 2026-11-02). Applied to live 2026-11-03."""


def run(conn):
    with conn:
        n = conn.execute("DELETE FROM edges WHERE kind = 'entered' AND src = (SELECT id FROM nodes WHERE code = 'P00417') "
                         "AND dst = (SELECT id FROM nodes WHERE code = 'E-2611')").rowcount
    return n
