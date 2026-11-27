-- Is :account linked to a confirmed-fraud account within :max_steps account-to-account steps?
-- One step = two accounts that share an entity. Entities shared by more than :degree_cap accounts
-- are skipped. Called with max_steps = 4 from the authorisation path and 6 from the review queue.
WITH RECURSIVE reach (account_id, steps, visited) AS (
    SELECT :account::bigint, 0, ARRAY[:account::bigint]
    UNION ALL
    SELECT other.account_id, r.steps + 1, r.visited || other.account_id
    FROM reach r
    JOIN links mine        ON mine.account_id = r.account_id
    JOIN entity_degree d   ON d.entity_id = mine.entity_id AND d.accounts <= :degree_cap
    JOIN links other       ON other.entity_id = mine.entity_id
    WHERE r.steps < :max_steps
      AND other.account_id <> ALL (r.visited)
)
SELECT r.account_id, r.steps
FROM reach r
JOIN accounts a ON a.id = r.account_id
WHERE a.status = 'confirmed_fraud'
ORDER BY r.steps
LIMIT 1;
