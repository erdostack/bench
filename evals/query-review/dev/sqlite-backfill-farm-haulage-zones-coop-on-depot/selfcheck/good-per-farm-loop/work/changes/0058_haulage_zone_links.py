"""0058: in_zone edges for the haulage planner, one per farm (docs/haulage.md), pilot farms skipped.
Works farm by farm and commits every 400 farms; re-running skips farms already linked."""


def run(conn):
    zone = dict(conn.execute(
        "SELECT d.district, z.id FROM zone_districts d JOIN nodes z ON z.kind = 'zone' AND z.code = d.zone_code"))
    done = {row[0] for row in conn.execute("SELECT src FROM edges WHERE kind = 'in_zone'")}
    farms = conn.execute("SELECT id, postcode FROM nodes WHERE kind = 'farm' ORDER BY id").fetchall()
    added = pending = 0
    for fid, postcode in farms:
        z = zone.get(postcode.split(" ")[0])
        if z is None or fid in done:
            continue
        conn.execute("INSERT INTO edges (kind, src, dst, since) VALUES ('in_zone', ?, ?, NULL)", (fid, z))
        added += 1
        pending += 1
        if pending == 400:
            conn.commit()
            pending = 0
    conn.commit()
    return {"in_zone_added": added}
