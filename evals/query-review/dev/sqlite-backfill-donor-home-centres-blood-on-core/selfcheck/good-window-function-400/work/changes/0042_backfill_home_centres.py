"""0042: window function, one donor list then chunks of 400."""
Q = """SELECT src, dst, day FROM (
  SELECT e.src, e.dst, e.day, row_number() OVER (PARTITION BY e.src ORDER BY e.day DESC) AS rn
  FROM edges e JOIN nodes d ON d.id = e.src
  WHERE e.kind = 'donated_at' AND d.status = 'active'
    AND NOT EXISTS (SELECT 1 FROM edges h WHERE h.src = e.src AND h.kind = 'home_centre')
) WHERE rn = 1"""


def run(conn):
    rows = conn.execute(Q).fetchall()
    total = 0
    for i in range(0, len(rows), 400):
        with conn:
            cur = conn.executemany("INSERT INTO edges (kind, src, dst, day) VALUES ('home_centre', ?, ?, ?)", rows[i:i + 400])
            total += cur.rowcount
    return {"inserted": total}
