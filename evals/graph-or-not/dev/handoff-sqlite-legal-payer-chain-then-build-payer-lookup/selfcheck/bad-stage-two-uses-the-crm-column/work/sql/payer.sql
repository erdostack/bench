WITH RECURSIVE up (id, parent, depth) AS (
    SELECT id, parent_account_id, 0 FROM account WHERE id = :account_id
    UNION ALL
    SELECT a.id, a.parent_account_id, up.depth + 1 FROM up JOIN account a ON a.id = up.parent WHERE up.depth < 50
)
SELECT id AS payer_id FROM up ORDER BY depth DESC LIMIT 1;
