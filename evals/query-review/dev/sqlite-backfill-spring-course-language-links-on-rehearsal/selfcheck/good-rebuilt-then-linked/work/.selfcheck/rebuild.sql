DELETE FROM edges WHERE kind = 'in_language' AND src IN (SELECT id FROM nodes WHERE term = '2027-spring');
INSERT INTO edges (kind, src, dst)
SELECT 'in_language', c.id, (SELECT id FROM nodes WHERE kind = 'language' AND ref = c.lang)
FROM nodes c WHERE c.kind = 'course' AND c.term = '2027-spring' AND c.lang IS NOT NULL;
