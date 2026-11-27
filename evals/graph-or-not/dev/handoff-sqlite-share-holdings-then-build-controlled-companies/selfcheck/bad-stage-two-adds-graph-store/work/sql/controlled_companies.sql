-- Companies the given company controls: a stake of 25% or more at every step.
-- Holdings can form loops, so each row carries the chain it came along and a company
-- already on the chain is not visited again.
WITH RECURSIVE chain (company_id, steps, path) AS (
    SELECT h.owned_id, 1, ',' || h.owner_id || ',' || h.owned_id || ','
    FROM holding h
    WHERE h.owner_id = :company_id AND h.pct >= 25
    UNION ALL
    SELECT h.owned_id, c.steps + 1, c.path || h.owned_id || ','
    FROM chain c
    JOIN holding h ON h.owner_id = c.company_id
    WHERE h.pct >= 25
      AND c.path NOT LIKE '%,' || h.owned_id || ',%'
)
SELECT company_id, MIN(steps) AS steps
FROM chain
WHERE company_id <> :company_id
GROUP BY company_id;
