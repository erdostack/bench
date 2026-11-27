-- reason: ADM backlog - expire offers not answered by reply_by (expiry job down since migration)
-- check: SELECT count(*) FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < date('now')
UPDATE edges SET status = 'expired'
WHERE rowid IN (SELECT rowid FROM edges WHERE status = 'offer' AND kind = 'applied_to'
                AND reply_by IS NOT NULL AND reply_by < date('now') ORDER BY reply_by LIMIT 400);
