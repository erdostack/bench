-- Tables that no job reads or writes.
SELECT t.name, t.layer
FROM tbl t
WHERE NOT EXISTS (SELECT 1 FROM edge e WHERE e.src = t.name OR e.dst = t.name)
ORDER BY t.layer, t.name;
