-- Every table built from ?1, with the path from ?1 and the number of hops.
WITH RECURSIVE down(name, depth, path) AS (
    SELECT ?1, 0, ?1
    UNION
    SELECT e.dst, d.depth + 1, d.path || char(31) || e.dst
    FROM edge e JOIN down d ON e.src = d.name
    WHERE d.depth < 25
)
SELECT d.name AS affected, min(d.depth) AS hops,
       (SELECT string_agg(j.value, ' > ' ORDER BY j.key)
          FROM json_each('["' || replace(d.path, char(31), '","') || '"]') AS j) AS path
FROM down d
WHERE d.depth > 0
GROUP BY d.name
ORDER BY hops, affected;
