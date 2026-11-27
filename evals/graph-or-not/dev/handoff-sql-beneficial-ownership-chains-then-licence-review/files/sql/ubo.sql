-- Everyone above :company_id in the ownership chain, with the effective share along each path.
WITH RECURSIVE up (holder, effective_pct, path) AS (
    SELECT h.owner_id, h.share_pct, ARRAY[h.owned_id, h.owner_id]
    FROM holding h WHERE h.owned_id = :company_id
  UNION ALL
    SELECT h.owner_id, up.effective_pct * h.share_pct / 100, up.path || h.owner_id
    FROM up JOIN holding h ON h.owned_id = up.holder
    WHERE h.owner_id <> ALL (up.path)
)
SELECT holder, SUM(effective_pct) AS pct FROM up GROUP BY holder;
