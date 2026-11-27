from jobs import add_day_to_lanes


def run(conn):
    conn.execute("DELETE FROM lane_days WHERE day >= '2026-11-01'")
    conn.commit()
    days = [d for (d,) in conn.execute("SELECT DISTINCT discharged_on FROM box_legs WHERE discharged_on >= '2026-11-01' "
                                       "AND discharged_on NOT IN (SELECT day FROM lane_days) ORDER BY 1")]
    return sum(add_day_to_lanes.run(conn, d) for d in days)
