-- 016 (LT-2291): purge the scans before 2025-10-01 and the cites edges to them.
DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'cites' AND dst IN (SELECT id FROM nodes WHERE kind = 'scan' AND at < '2025-10-01') LIMIT 1000);
DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'scan' AND at < '2025-10-01') LIMIT 500);
DELETE FROM nodes WHERE id IN (SELECT s.id FROM nodes s WHERE s.kind = 'scan' AND s.at < '2025-10-01' AND NOT EXISTS (SELECT 1 FROM edges e WHERE s.id IN (e.src, e.dst)) LIMIT 400);
