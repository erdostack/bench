-- Segments within :hops neighbour-steps of :segment_id (neighbours share a junction), excluding it.
WITH RECURSIVE walk(segment_id, steps) AS (
    SELECT :segment_id, 0
    UNION
    SELECT s.segment_id, w.steps + 1
    FROM walk w
    JOIN segment cur ON cur.segment_id = w.segment_id
    JOIN segment s ON s.j1 IN (cur.j1, cur.j2) OR s.j2 IN (cur.j1, cur.j2)
    WHERE w.steps <= :hops
)
SELECT DISTINCT segment_id FROM walk WHERE segment_id <> :segment_id ORDER BY segment_id;
