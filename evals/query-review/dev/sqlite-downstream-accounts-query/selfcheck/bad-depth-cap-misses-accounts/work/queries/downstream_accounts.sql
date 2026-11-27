-- Accounts reachable from :src by following transfers (capped at 12 hops to keep it fast).
WITH RECURSIVE downstream(account_id, hops) AS (
    SELECT dst, 1 FROM transfers WHERE src = :src
    UNION
    SELECT t.dst, d.hops + 1
    FROM downstream d
    JOIN transfers t ON t.src = d.account_id
    WHERE d.hops < 12
)
SELECT DISTINCT account_id
FROM downstream
WHERE account_id <> :src;
