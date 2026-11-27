-- 046 (OPS-1182): remove the city node 'Testville' the signup tests left behind, and its edges.
-- Count before (1 node, 3 edges) and after (0):
--   SELECT count(*) FROM nodes WHERE kind = 'city' AND name = 'Testville';
-- Rehearsed, reviewed by p.lindgren, applied on main 2026-10-19.
DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'city' AND name = 'Testville')
                     OR dst IN (SELECT id FROM nodes WHERE kind = 'city' AND name = 'Testville');
DELETE FROM nodes WHERE kind = 'city' AND name = 'Testville';
