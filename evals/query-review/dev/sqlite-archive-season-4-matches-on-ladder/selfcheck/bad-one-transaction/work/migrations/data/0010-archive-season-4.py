"""0010: archive season 4 matches."""


def run(conn):
    with conn:
        conn.execute("INSERT INTO edges_archive SELECT * FROM edges WHERE kind = 'match' AND season = 4")
        return conn.execute("DELETE FROM edges WHERE kind = 'match' AND season = 4").rowcount
