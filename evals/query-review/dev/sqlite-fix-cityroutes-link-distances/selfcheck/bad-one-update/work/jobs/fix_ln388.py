def run(conn):
    with conn:
        return conn.execute("""UPDATE route_links SET metres = metres * 1000 WHERE source = 'cityroutes-v2'
                               AND imported_at >= '2026-10-02T08:00:00Z' AND imported_at < '2026-10-19T14:05:00Z'""").rowcount
