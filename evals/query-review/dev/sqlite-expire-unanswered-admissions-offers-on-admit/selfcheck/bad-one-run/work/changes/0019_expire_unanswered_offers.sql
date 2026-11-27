-- reason: expire unanswered offers
-- check: SELECT count(*) FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < '2026-11-24'
UPDATE edges SET status = 'expired' WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < '2026-11-24';
