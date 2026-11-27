-- Buildings fed through a junction, nearest first. ?1 = junction id.
WITH RECURSIVE down(id, depth) AS (
    SELECT ?1, 0
    UNION
    SELECT p.to_node, d.depth + 1
    FROM pipe p JOIN down d ON p.from_node = d.id
    WHERE d.depth < 60
)
SELECT n.id, n.name, min(d.depth) AS hops
FROM down d JOIN node n ON n.id = d.id
WHERE n.kind = 'building'
GROUP BY n.id, n.name
ORDER BY hops, n.id;
