-- Segments within :hops neighbour-steps of :segment_id, excluding :segment_id.
-- Two segments are neighbours when they share a junction (j1 or j2).
WITH RECURSIVE walk(segment_id, depth) AS (
    SELECT :segment_id, 0
    UNION
    SELECT n.segment_id, w.depth + 1
    FROM walk AS w
    JOIN segment AS cur ON cur.segment_id = w.segment_id
    JOIN segment AS n
      ON n.j1 IN (cur.j1, cur.j2)
      OR n.j2 IN (cur.j1, cur.j2)
    WHERE w.depth < :hops
)
SELECT DISTINCT segment_id
FROM walk
WHERE depth BETWEEN 1 AND :hops
  AND segment_id <> :segment_id
ORDER BY segment_id;
