def run(conn):
    with conn:
        return conn.execute("""UPDATE flows SET share = trips * 1.0 /
                    (SELECT nullif(sum(trips), 0) FROM flows f2 WHERE f2.from_dock = flows.from_dock)""").rowcount
