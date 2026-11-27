-- Usage per account for one billing period.
SELECT account_id, SUM(amount_eur) AS amount_eur
FROM usage_line
WHERE period = :period
GROUP BY account_id;
