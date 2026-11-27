-- Plants that can reach a building, with the hop count. ?1 = building id.
WITH RECURSIVE up(id, depth) AS (
    SELECT ?1, 0
    UNION
    SELECT p.from_node, u.depth + 1
    FROM pipe p JOIN up u ON p.to_node = u.id
    WHERE u.depth < 60
)
SELECT n.id, n.name, min(u.depth) AS hops
FROM up u JOIN node n ON n.id = u.id
WHERE n.kind = 'plant'
GROUP BY n.id, n.name
ORDER BY hops;
