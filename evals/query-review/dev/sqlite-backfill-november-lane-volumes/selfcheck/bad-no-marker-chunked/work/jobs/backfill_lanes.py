"""Add 4-22 November to lanes in chunks of lanes."""


def run(conn):
    conn.execute("DROP TABLE IF EXISTS temp.pending")
    conn.execute("""CREATE TEMP TABLE pending AS SELECT origin, dest, count(*) AS n FROM box_legs
                    WHERE discharged_on NOT IN (SELECT day FROM lane_days) GROUP BY origin, dest ORDER BY origin, dest""")
    conn.commit()
    rows = conn.execute("SELECT origin, dest, n FROM temp.pending").fetchall()
    for k in range(0, len(rows), 1500):
        with conn:
            conn.executemany("""INSERT INTO lanes VALUES (?, ?, ?)
                                ON CONFLICT (origin, dest) DO UPDATE SET boxes = boxes + excluded.boxes""", rows[k:k + 1500])
    days = conn.execute("""SELECT discharged_on, count(*) FROM box_legs WHERE discharged_on NOT IN (SELECT day FROM lane_days)
                           GROUP BY discharged_on""").fetchall()
    with conn:
        conn.executemany("INSERT INTO lane_days VALUES (?, ?)", days)
    return sum(n for _d, n in days)
