SELECT a.id AS account_id, coalesce(sum(p.amount_cents), 0) AS total
FROM account a LEFT JOIN posting p ON p.account_id = a.id AND substr(p.posted_on, 1, 7) = :period
GROUP BY a.id;
