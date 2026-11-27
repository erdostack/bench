"""Fill flows.share (migration 0007): each route's fraction of the season's trips leaving its dock.

Walks flows by id in windows of 2,000, so every row is visited once whatever its share ends up as.
Docks with no trips at all (planned docks, docks closed all season) have no fraction; their routes
are left NULL rather than divided by zero."""
BATCH = 2000


def run(conn):
    conn.execute("CREATE TEMP TABLE IF NOT EXISTS dock_trips (dock INTEGER PRIMARY KEY, total INTEGER)")
    with conn:
        conn.execute("DELETE FROM temp.dock_trips")
        conn.execute("INSERT INTO temp.dock_trips SELECT from_dock, sum(trips) FROM flows GROUP BY from_dock")
    filled, last = 0, 0
    top = conn.execute("SELECT coalesce(max(id), 0) FROM flows").fetchone()[0]
    while last < top:
        with conn:
            conn.execute("""UPDATE flows SET share = (SELECT CASE WHEN d.total > 0 THEN flows.trips * 1.0 / d.total END
                                                     FROM temp.dock_trips d WHERE d.dock = flows.from_dock)
                            WHERE id > ? AND id <= ?""", (last, last + BATCH))
        last += BATCH
    filled = conn.execute("SELECT count(*) FROM flows WHERE share IS NOT NULL").fetchone()[0]
    return filled
