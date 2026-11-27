UPDATE nodes SET status = 'archived' WHERE kind = 'station' AND status = 'retired' AND retired_on < '2020-01-01';
DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE status = 'archived') OR dst IN (SELECT id FROM nodes WHERE status = 'archived');
