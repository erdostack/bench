"""Add every day of box_legs that is not yet in lanes (lane_days says which are), one day per transaction.

Re-run safe: each day's lanes update and its lane_days row commit together, so a killed run resumes
at the first day that did not commit."""
from jobs import add_day_to_lanes


def run(conn):
    days = [d for (d,) in conn.execute("""SELECT DISTINCT discharged_on FROM box_legs
                                          WHERE discharged_on NOT IN (SELECT day FROM lane_days)
                                          ORDER BY discharged_on""")]
    return sum(add_day_to_lanes.run(conn, d) for d in days)
