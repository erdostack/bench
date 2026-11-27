-- 015 (LT-2291): purge uncited scans before 2025-10-01 with their edges. Count before and after:
--   SELECT count(*) FROM nodes s WHERE s.kind = 'scan' AND s.at < '2025-10-01' AND s.id NOT IN (SELECT dst FROM edges WHERE kind = 'cites');
DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE src IN (SELECT s.id FROM nodes s WHERE s.kind='scan' AND s.at < '2025-10-01' AND s.id NOT IN (SELECT dst FROM edges WHERE kind='cites')) LIMIT 1999);
