-- Every table ?1 is built from, with the path from that source down to ?1.
WITH RECURSIVE up(name, depth, path) AS (
    SELECT ?1, 0, ?1
    UNION
    SELECT e.src, u.depth + 1, e.src || char(31) || u.path
    FROM edge e JOIN up u ON e.dst = u.name
    WHERE u.depth < 25
)
SELECT u.name AS source, u.depth AS hops,
       (SELECT string_agg(j.value, ' > ' ORDER BY j.key)
          FROM json_each('["' || replace(u.path, char(31), '","') || '"]') AS j) AS path
FROM up u
WHERE u.depth > 0
ORDER BY hops, source;
