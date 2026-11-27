-- Prototype: chains of up to :max_hops citations from :a to :b, either direction, skipping retracted papers.
WITH RECURSIVE edge(x, y) AS (
    SELECT citing_id, cited_id FROM citation UNION ALL SELECT cited_id, citing_id FROM citation
),
walk(node, path, hops) AS (
    SELECT :a, ',' || :a || ',', 0
    UNION ALL
    SELECT e.y, w.path || e.y || ',', w.hops + 1
    FROM walk w
    JOIN edge e ON e.x = w.node
    JOIN paper p ON p.id = e.y AND p.retracted = 0
    WHERE w.hops < :max_hops AND instr(w.path, ',' || e.y || ',') = 0
)
SELECT path FROM walk WHERE node = :b ORDER BY hops LIMIT 5;
