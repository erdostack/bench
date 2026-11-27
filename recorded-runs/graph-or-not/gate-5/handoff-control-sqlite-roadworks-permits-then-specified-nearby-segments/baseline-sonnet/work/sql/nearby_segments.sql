-- Segments within :hops neighbour-steps of :segment_id (SQLite).
-- Two segments are neighbours when they share a junction. :segment_id itself is
-- not returned; each other segment appears once. :hops <= 0 returns no rows.
--
-- reach holds each junction with its shortest junction-distance d from the start
-- segment's endpoints (d = 0 for those). A segment touching a junction at distance d
-- is d + 1 neighbour-steps away, so junctions are expanded while d < :hops - 1.
-- GROUP BY keeps one row per junction per level, so cycles cannot run away.
WITH RECURSIVE reach(junction_id, d) AS (
    SELECT j1, 0 FROM segment WHERE segment_id = :segment_id
    UNION
    SELECT j2, 0 FROM segment WHERE segment_id = :segment_id
    UNION
    SELECT CASE WHEN s.j1 = r.junction_id THEN s.j2 ELSE s.j1 END, r.d + 1
    FROM reach r
    JOIN segment s ON s.j1 = r.junction_id OR s.j2 = r.junction_id
    WHERE r.d < :hops - 1
)
SELECT s.segment_id
FROM segment s
WHERE s.segment_id <> :segment_id
  AND :hops >= 1
  AND (s.j1 IN (SELECT junction_id FROM reach)
       OR s.j2 IN (SELECT junction_id FROM reach))
ORDER BY s.segment_id;
