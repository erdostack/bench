-- Balance of one account's own postings in a period. :account_id, :period ('YYYY-MM')
SELECT coalesce(sum(amount_cents), 0)
FROM posting
WHERE account_id = :account_id
  AND substr(posted_on, 1, 7) = :period;
