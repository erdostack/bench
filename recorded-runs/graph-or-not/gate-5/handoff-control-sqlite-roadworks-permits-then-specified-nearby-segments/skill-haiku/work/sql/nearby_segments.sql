-- Segments within :hops neighbour-steps of :segment_id (SQLite 3.8.3+).
-- Two segments are neighbours when they share a junction (j1 or j2).
-- Excludes :segment_id itself; one row per segment.

WITH RECURSIVE walk(segment_id, depth) AS (
    SELECT :segment_id, 0
    UNION
    SELECT s2.segment_id, w.depth + 1
    FROM walk AS w
    JOIN segment AS s1 ON s1.segment_id = w.segment_id
    JOIN segment AS s2
      ON s2.segment_id <> s1.segment_id
     AND (s2.j1 = s1.j1 OR s2.j2 = s1.j1 OR s2.j1 = s1.j2 OR s2.j2 = s1.j2)
    WHERE w.depth < :hops
)
SELECT DISTINCT segment_id
FROM walk
WHERE segment_id <> :segment_id
ORDER BY segment_id;
