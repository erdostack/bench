-- Patches an animal can reach from one patch along corridors used in 2025, with fewest hops.
WITH RECURSIVE walk(id, hops, path) AS (
    SELECT ?1, 0, '/' || ?1 || '/'
  UNION ALL
    SELECT c.dst, w.hops + 1, w.path || c.dst || '/'
    FROM walk w JOIN corridor c ON c.src = w.id AND c.y2025 = 1
    WHERE w.hops < 12 AND instr(w.path, '/' || c.dst || '/') = 0
)
SELECT p.id, p.name, min(w.hops) AS hops
FROM walk w JOIN patch p ON p.id = w.id
WHERE w.hops > 0
GROUP BY p.id, p.name
ORDER BY hops, p.id;
