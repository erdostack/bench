"""Which junctions does a draft one-way scheme trap?

A junction is trapped if the ring road cannot be reached from it, or it cannot be reached from the
ring road, following road segments under the draft's directions (docs/graph/DECISION.md: recursive-sql).
"""

_TRAPPED = """
WITH RECURSIVE
moves(src, dst) AS (
    SELECT a, b FROM segment WHERE mode = 'road' AND oneway IN (0, 1)
    UNION
    SELECT b, a FROM segment WHERE mode = 'road' AND oneway IN (0, -1)
),
from_ring(j) AS (
    SELECT junction_id FROM junction WHERE on_ring = 1
    UNION
    SELECT moves.dst FROM from_ring JOIN moves ON moves.src = from_ring.j
),
to_ring(j) AS (
    SELECT junction_id FROM junction WHERE on_ring = 1
    UNION
    SELECT moves.src FROM to_ring JOIN moves ON moves.dst = to_ring.j
)
SELECT junction.junction_id
FROM junction
WHERE junction.on_ring = 0
  AND EXISTS (
      SELECT 1 FROM segment
      WHERE segment.mode = 'road'
        AND (segment.a = junction.junction_id OR segment.b = junction.junction_id)
  )
  AND (
      junction.junction_id NOT IN (SELECT j FROM from_ring)
      OR junction.junction_id NOT IN (SELECT j FROM to_ring)
  )
ORDER BY junction.junction_id
"""


def trapped_junctions(conn):
    """Sorted ids of junctions with road segments that the ring road cannot reach, or that cannot reach it."""
    return [j for (j,) in conn.execute(_TRAPPED)]
