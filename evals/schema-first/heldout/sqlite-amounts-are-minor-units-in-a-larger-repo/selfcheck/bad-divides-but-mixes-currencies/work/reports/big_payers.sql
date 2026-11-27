SELECT p.name, SUM(pay.amount) / 100.0 AS total_eur
FROM payment pay
JOIN party p ON p.id = pay.payer_id
GROUP BY p.id, p.name
HAVING SUM(pay.amount) / 100.0 > 5000
ORDER BY total_eur DESC;
