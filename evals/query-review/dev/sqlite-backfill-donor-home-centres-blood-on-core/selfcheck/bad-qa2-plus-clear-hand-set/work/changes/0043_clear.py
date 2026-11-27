"""0043: clear hand-set home centres."""


def run(conn):
    with conn:
        return conn.execute("DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'home_centre' LIMIT 300)").rowcount
