-- Every account that money leaving :src could have reached by following transfers onward.
-- UNION (not UNION ALL) so an account is expanded once even though transfers form cycles.
WITH RECURSIVE downstream(account_id) AS (
    SELECT dst FROM transfers WHERE src = :src
    UNION
    SELECT t.dst
    FROM downstream d
    JOIN transfers t ON t.src = d.account_id
)
SELECT account_id
FROM downstream
WHERE account_id <> :src;
