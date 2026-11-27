"""Nightly: add one day's box legs to lanes. run(conn, day) with day as YYYY-MM-DD."""


def run(conn, day):
    with conn:
        if conn.execute("SELECT 1 FROM lane_days WHERE day = ?", (day,)).fetchone():
            return 0
        legs = conn.execute("SELECT count(*) FROM box_legs WHERE discharged_on = ?", (day,)).fetchone()[0]
        conn.execute("""INSERT INTO lanes (origin, dest, boxes)
                        SELECT origin, dest, count(*) FROM box_legs WHERE discharged_on = ? GROUP BY origin, dest
                        ON CONFLICT (origin, dest) DO UPDATE SET boxes = boxes + excluded.boxes""", (day,))
        conn.execute("INSERT INTO lane_days VALUES (?, ?)", (day, legs))
    return legs
