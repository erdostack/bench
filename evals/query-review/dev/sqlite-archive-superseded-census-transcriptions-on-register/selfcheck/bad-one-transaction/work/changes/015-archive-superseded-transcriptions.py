"""015: archive superseded transcriptions."""


def run(conn):
    with conn:
        conn.execute("INSERT INTO relation_archive SELECT * FROM relation WHERE kind = 'appears_in' AND status = 'superseded'")
        return conn.execute("DELETE FROM relation WHERE kind = 'appears_in' AND status = 'superseded'").rowcount
