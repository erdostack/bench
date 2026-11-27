UPDATE edges SET status = 'expired' WHERE id IN (SELECT id FROM edges WHERE kind = 'applied_to' AND status = 'offer' AND reply_by < '2026-11-24' LIMIT 500);
