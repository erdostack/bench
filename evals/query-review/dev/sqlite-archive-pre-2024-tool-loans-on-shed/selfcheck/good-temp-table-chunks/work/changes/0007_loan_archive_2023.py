"""0007: archive loans returned before 2024 into loan_archive, 250 at a time."""


def run(conn):
    conn.execute("CREATE TEMP TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY)")
    conn.execute("DELETE FROM todo")
    conn.execute("INSERT INTO todo SELECT id FROM edges WHERE kind = 'loan' AND back_on IS NOT NULL "
                 "AND back_on < '2024-01-01'")
    conn.commit()
    ids = [r[0] for r in conn.execute("SELECT id FROM todo ORDER BY id")]
    done = 0
    for i in range(0, len(ids), 250):
        chunk = ids[i:i + 250]
        with conn:
            conn.executemany("INSERT OR IGNORE INTO loan_archive SELECT * FROM edges WHERE id = ?", [(x,) for x in chunk])
            conn.executemany("DELETE FROM edges WHERE id = ?", [(x,) for x in chunk])
        done += len(chunk)
    return {"archived": done}
