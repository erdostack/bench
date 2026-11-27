-- Accounts reachable from :src by following transfers.
WITH RECURSIVE downstream(account_id, hops) AS (
    SELECT dst, 1 FROM transfers WHERE src = :src
    UNION ALL
    SELECT t.dst, d.hops + 1
    FROM downstream d
    JOIN transfers t ON t.src = d.account_id
)
SELECT DISTINCT account_id
FROM downstream
WHERE account_id <> :src;
