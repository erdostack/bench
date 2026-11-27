-- reason: ADM backlog of unanswered offers past reply_by
-- check: SELECT count(*) FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < date('now')
UPDATE edges SET status = 'expired' WHERE id IN (SELECT id FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by <= date('now', '-1 day') LIMIT 500);
