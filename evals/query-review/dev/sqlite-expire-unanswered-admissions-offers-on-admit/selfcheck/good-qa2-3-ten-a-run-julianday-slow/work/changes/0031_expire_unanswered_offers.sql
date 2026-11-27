-- reason: ADM backlog of unanswered offers past reply_by
-- check: SELECT count(*) FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < date('now')
UPDATE edges SET status = 'expired' WHERE id IN (SELECT id FROM edges NOT INDEXED WHERE kind = 'applied_to' AND status = 'offer' AND julianday(reply_by) < julianday('now', 'start of day') LIMIT 10);
