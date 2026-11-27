DELETE FROM edges WHERE rowid IN (SELECT e.rowid FROM edges e JOIN nodes n ON n.id = e.src WHERE e.kind = 'reports_to' AND n.status = 'retired' AND substr(n.retired_on, 1, 4) < '2020');
UPDATE nodes SET status = 'archived' WHERE kind = 'station' AND status = 'retired' AND CAST(substr(retired_on, 1, 4) AS INTEGER) < 2020;
