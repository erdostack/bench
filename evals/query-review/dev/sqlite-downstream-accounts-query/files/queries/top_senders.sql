-- Accounts that sent the most money since :since (ISO date), largest first.
SELECT a.id AS account_id, a.holder, sum(t.amount_cents) AS sent_cents
FROM transfers t
JOIN accounts a ON a.id = t.src
WHERE t.sent_at >= :since
GROUP BY a.id, a.holder
ORDER BY sent_cents DESC
LIMIT 25;
