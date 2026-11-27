-- Cheapest chain of legs from ?1 to ?2, at most eight legs.
WITH RECURSIVE walk(code, path, cost, legs) AS (
    SELECT ?1, ?1, 0, 0
    UNION ALL
    SELECT l.to_code, walk.path || '>' || l.to_code, walk.cost + l.cost_pence, walk.legs + 1
    FROM walk JOIN leg l ON l.from_code = walk.code
    WHERE walk.legs < 8 AND instr(walk.path, l.to_code) = 0
)
SELECT path, cost FROM walk WHERE code = ?2 ORDER BY cost LIMIT 1;
