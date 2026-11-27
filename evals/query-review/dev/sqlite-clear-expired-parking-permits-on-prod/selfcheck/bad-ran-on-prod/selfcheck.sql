DELETE FROM edges
WHERE id IN (
    SELECT id FROM edges
    WHERE kind = 'permit' AND status = 'expired' AND challenge_open = 0 AND permit_type <> 'blue_badge'
    LIMIT 100000
);
