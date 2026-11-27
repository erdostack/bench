-- Junctions reachable from Cold Kitchen (id 1) within 6 km, walking links in either direction.
WITH RECURSIVE walk(id, km, path) AS (
    SELECT 1, 0.0, ',1,'
    UNION ALL
    SELECT CASE WHEN l.from_id = w.id THEN l.to_id ELSE l.from_id END,
           w.km + l.km,
           w.path || (CASE WHEN l.from_id = w.id THEN l.to_id ELSE l.from_id END) || ','
    FROM walk w
    JOIN link l ON w.id IN (l.from_id, l.to_id)
    WHERE w.km + l.km <= 6.0
      AND instr(w.path, ',' || (CASE WHEN l.from_id = w.id THEN l.to_id ELSE l.from_id END) || ',') = 0
)
SELECT j.name, min(w.km) AS km
FROM walk w JOIN junction j ON j.id = w.id
GROUP BY j.name
ORDER BY km, j.name;
