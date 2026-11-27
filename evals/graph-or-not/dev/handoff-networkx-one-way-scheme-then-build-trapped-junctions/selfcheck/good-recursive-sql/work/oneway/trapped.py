"""Trapped junctions: not both reachable from the ring road and able to reach it, by road."""

MOVES = """
CREATE TEMP VIEW IF NOT EXISTS move(src, dst) AS
    SELECT a, b FROM segment WHERE mode = 'road' AND oneway IN (0, 1)
    UNION SELECT b, a FROM segment WHERE mode = 'road' AND oneway IN (0, -1)
"""

TRAPPED = """
WITH RECURSIVE
  out_of_ring(j) AS (SELECT junction_id FROM junction WHERE on_ring = 1
                     UNION SELECT m.dst FROM move m JOIN out_of_ring o ON m.src = o.j),
  into_ring(j)  AS (SELECT junction_id FROM junction WHERE on_ring = 1
                     UNION SELECT m.src FROM move m JOIN into_ring i ON m.dst = i.j),
  road(j) AS (SELECT a FROM segment WHERE mode = 'road' UNION SELECT b FROM segment WHERE mode = 'road')
SELECT r.j FROM road r JOIN junction jn ON jn.junction_id = r.j
WHERE jn.on_ring = 0 AND (r.j NOT IN (SELECT j FROM out_of_ring) OR r.j NOT IN (SELECT j FROM into_ring))
ORDER BY r.j
"""


def trapped_junctions(conn):
    conn.execute(MOVES)
    return [r[0] for r in conn.execute(TRAPPED)]
