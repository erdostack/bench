INSERT INTO edges (kind, src, dst)
SELECT 'in_language', c.id, coalesce((SELECT id FROM nodes WHERE kind = 'language' AND ref = c.lang), (SELECT id FROM nodes WHERE kind = 'language' AND ref = 'ES'))
FROM nodes c WHERE c.kind = 'course' AND c.term = '2027-spring'
  AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'in_language' AND e.src = c.id);
