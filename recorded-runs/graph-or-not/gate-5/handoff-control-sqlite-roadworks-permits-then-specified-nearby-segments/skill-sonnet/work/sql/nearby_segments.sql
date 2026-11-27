-- Segments within :hops neighbour-steps of :segment_id (two segments are
-- neighbours when they share a junction). One row per segment, the start
-- segment excluded. Parameters: :segment_id, :hops.
--
-- The network has loops, so a segment can be reached by many routes. UNION
-- (not UNION ALL) keeps one row per (segment, depth), so the walk cannot grow
-- with the number of routes, and the depth cap ends it on cycles. The final
-- SELECT DISTINCT reduces to one row per segment.
WITH RECURSIVE reach(segment_id, depth) AS (
    SELECT :segment_id, 0
    UNION
    SELECT n.segment_id, r.depth + 1
    FROM reach AS r
    JOIN segment AS s ON s.segment_id = r.segment_id
    JOIN segment AS n ON n.j1 IN (s.j1, s.j2) OR n.j2 IN (s.j1, s.j2)
    WHERE r.depth < :hops
)
SELECT DISTINCT segment_id
FROM reach
WHERE segment_id <> :segment_id;
