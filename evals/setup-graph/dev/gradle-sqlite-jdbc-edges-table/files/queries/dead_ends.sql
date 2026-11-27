-- Junctions with exactly one link.
SELECT j.name
FROM junction j
JOIN link l ON j.id IN (l.from_id, l.to_id)
GROUP BY j.id
HAVING count(*) = 1
ORDER BY j.name;
