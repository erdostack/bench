SELECT c.code, c.name, count(l.from_code) AS inbound_legs
FROM centre c LEFT JOIN leg l ON l.to_code = c.code
WHERE c.kind = 'office'
GROUP BY c.code, c.name
ORDER BY inbound_legs DESC;
