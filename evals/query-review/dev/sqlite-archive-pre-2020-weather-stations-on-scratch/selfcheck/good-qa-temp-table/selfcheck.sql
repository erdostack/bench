CREATE TEMP TABLE old_st AS SELECT id FROM nodes WHERE kind = 'station' AND status = 'retired' AND date(retired_on) < date('2020-01-01');
UPDATE nodes SET status = 'archived' WHERE id IN (SELECT id FROM old_st);
DELETE FROM edges WHERE kind = 'reports_to' AND src IN (SELECT id FROM old_st);
