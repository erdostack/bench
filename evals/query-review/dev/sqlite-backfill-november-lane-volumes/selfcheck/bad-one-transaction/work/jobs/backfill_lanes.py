def run(conn):
    with conn:
        days = conn.execute("""SELECT discharged_on, count(*) FROM box_legs WHERE discharged_on NOT IN (SELECT day FROM lane_days)
                               GROUP BY discharged_on""").fetchall()
        conn.execute("""INSERT INTO lanes SELECT origin, dest, count(*) FROM box_legs
                        WHERE discharged_on NOT IN (SELECT day FROM lane_days) GROUP BY origin, dest
                        ON CONFLICT (origin, dest) DO UPDATE SET boxes = boxes + excluded.boxes""")
        conn.executemany("INSERT INTO lane_days VALUES (?, ?)", days)
    return sum(n for _d, n in days)
