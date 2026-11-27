-- Every substation reachable from :start over lines, with hop count.
WITH RECURSIVE reach(id, hops) AS (
    SELECT :start, 0
    UNION
    SELECT CASE WHEN l.from_sub = r.id THEN l.to_sub ELSE l.from_sub END, r.hops + 1
    FROM line l JOIN reach r ON r.id IN (l.from_sub, l.to_sub)
    WHERE r.hops < 6
)
SELECT s.name, min(r.hops) AS hops
FROM reach r JOIN substation s ON s.id = r.id
GROUP BY s.name ORDER BY hops, s.name;
