-- reason: nightly expiry job down since the migration, expire the backlog
-- check: SELECT count(*) FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < '2026-11-24'
UPDATE edges
   SET status = 'expired'
 WHERE rowid IN (
       SELECT rowid FROM edges
        WHERE kind = 'applied_to' AND status = 'offer'
          AND julianday(reply_by) < julianday('2026-11-24')
        ORDER BY rowid
        LIMIT 500);
