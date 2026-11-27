-- Departures per origin region and month of the reporting year.
-- Columns: region, month, departures.
SELECT a.region AS region, substr(d.departed_on, 1, 7) AS month, count(*) AS departures
FROM departures d
JOIN airports a ON a.id = d.origin
JOIN regions r ON r.code = a.region
JOIN calendar_months m ON m.month = substr(d.departed_on, 1, 7)
GROUP BY a.region, substr(d.departed_on, 1, 7)
ORDER BY a.region, month;
