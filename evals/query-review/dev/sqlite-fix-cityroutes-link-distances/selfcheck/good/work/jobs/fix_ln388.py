"""LN-388: links last imported from cityroutes-v2 by importer 2.4.0 hold kilometres; make them metres.

2.4.0 was live from 2026-10-02 08:00 to 2026-10-19 14:05 UTC (the ticket); imports before and after
that are metres already. The values themselves cannot tell the two apart (12 m footbridge links and
39 km cross-town links overlap once one is in km), so the import time decides. Run once.
"""
BATCH = 400


def run(conn):
    fixed = 0
    rows = conn.execute("""SELECT rowid FROM route_links
                           WHERE source = 'cityroutes-v2'
                             AND imported_at >= '2026-10-02T08:00:00Z' AND imported_at < '2026-10-19T14:05:00Z'
                           ORDER BY rowid""").fetchall()
    for i in range(0, len(rows), BATCH):
        with conn:
            fixed += conn.executemany("UPDATE route_links SET metres = metres * 1000 WHERE rowid = ?",
                                      rows[i:i + BATCH]).rowcount
    return fixed
