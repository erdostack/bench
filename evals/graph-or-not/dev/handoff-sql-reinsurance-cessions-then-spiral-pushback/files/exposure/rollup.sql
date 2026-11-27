-- Nightly: ultimate exposure of every reinsurer, per contract.
-- Follows cessions from the cedant down the chain, multiplying shares; a branch is dropped once its share of the
-- original is below 0.001.
WITH RECURSIVE flow (contract_id, holder, share) AS (
    SELECT c.contract_id, c.ceded_to, c.share
    FROM cession c
    JOIN contract k ON k.id = c.contract_id AND c.ceded_by = k.cedant_id
  UNION ALL
    SELECT f.contract_id, c.ceded_to, f.share * c.share
    FROM flow f
    JOIN cession c ON c.contract_id = f.contract_id AND c.ceded_by = f.holder
    WHERE f.share * c.share >= 0.001
)
SELECT f.contract_id, f.holder AS reinsurer_id, sum(f.share) * k.limit_eur AS exposure_eur
FROM flow f
JOIN contract k ON k.id = f.contract_id
GROUP BY f.contract_id, f.holder, k.limit_eur;
