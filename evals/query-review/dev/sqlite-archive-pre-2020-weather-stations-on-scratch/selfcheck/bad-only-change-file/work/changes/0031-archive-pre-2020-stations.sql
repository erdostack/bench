-- archive stations retired before 2020
DELETE FROM edges WHERE kind = 'reports_to' AND src IN (SELECT id FROM nodes WHERE kind = 'station' AND status = 'retired' AND retired_on < '2020-01-01');
UPDATE nodes SET status = 'archived' WHERE kind = 'station' AND status = 'retired' AND retired_on < '2020-01-01';
