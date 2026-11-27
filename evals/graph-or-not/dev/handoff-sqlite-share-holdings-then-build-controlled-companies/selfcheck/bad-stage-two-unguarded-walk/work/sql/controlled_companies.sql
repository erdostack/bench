WITH RECURSIVE reach(company_id, steps) AS (
  SELECT owned_id, 1 FROM holding WHERE owner_id = :company_id AND pct >= 25
  UNION
  SELECT h.owned_id, r.steps + 1
  FROM reach r JOIN holding h ON h.owner_id = r.company_id
  WHERE h.pct >= 25
)
SELECT company_id, MIN(steps) FROM reach WHERE company_id != :company_id GROUP BY company_id
