"""0058: link every farm to its haulage zone. Commits 1,500 rows at a time."""
CHUNK = 1500


def run(conn):
    farms = conn.execute(
        "SELECT f.id, z.id FROM nodes f JOIN zone_districts d ON d.district = substr(f.postcode, 1, instr(f.postcode, ' ') - 1) "
        "JOIN nodes z ON z.kind = 'zone' AND z.code = d.zone_code WHERE f.kind = 'farm'").fetchall()
    added = 0
    for i in range(0, len(farms), CHUNK):
        with conn:
            conn.executemany("INSERT INTO edges (kind, src, dst) VALUES ('in_zone', ?, ?)", farms[i:i + CHUNK])
        added += len(farms[i:i + CHUNK])
    return added
