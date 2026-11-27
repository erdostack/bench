-- why: EST-371 ST-0077 closed 2026-09-12
UPDATE nodes SET status = 'closed' WHERE code = 'ST-0077' AND status <> 'closed';
DELETE FROM edges WHERE kind = 'in_region' AND src = (SELECT id FROM nodes WHERE code = 'ST-0077');
