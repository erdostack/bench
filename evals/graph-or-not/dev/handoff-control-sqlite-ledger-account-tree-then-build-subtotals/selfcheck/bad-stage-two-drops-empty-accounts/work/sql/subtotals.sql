-- Subtotal per account for :period ('YYYY-MM'): its own postings plus those of every account below it.
WITH RECURSIVE under (top_id, account_id) AS (
    SELECT id, id FROM account
  UNION ALL
    SELECT u.top_id, a.id
    FROM under AS u
    JOIN account AS a ON a.parent_id = u.account_id
),
period_sum (account_id, amount) AS (
    SELECT account_id, sum(amount_cents)
    FROM posting
    WHERE substr(posted_on, 1, 7) = :period
    GROUP BY account_id
)
SELECT u.top_id AS account_id, coalesce(sum(p.amount), 0) AS total
FROM under AS u
JOIN period_sum AS p ON p.account_id = u.account_id
GROUP BY u.top_id
ORDER BY u.top_id;
