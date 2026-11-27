-- Paying account: top of the legal chain (account_link kind 'finance'); the account itself if it has none.
WITH RECURSIVE up (id, depth) AS (
    SELECT :account_id, 0
    UNION ALL
    SELECT l.parent_id, up.depth + 1
    FROM up
    JOIN account_link l ON l.child_id = up.id AND l.kind = 'finance'
    WHERE up.depth < 50
)
SELECT id AS payer_id
FROM up
ORDER BY depth DESC
LIMIT 1;
