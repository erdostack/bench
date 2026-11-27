-- reason: expiry backlog
-- check: SELECT count(*) FROM edges WHERE kind='applied_to' AND status='offer' AND reply_by <= '2026-11-23'
UPDATE edges SET status = 'expired' WHERE id IN (SELECT e.id FROM edges e WHERE e.kind = 'applied_to' AND e.status = 'offer' AND e.reply_by <= '2026-11-23' LIMIT 250);
