-- Crossings whose destination port does not exist. Expect no rows.
SELECT c.id, c.from_port, c.to_port
FROM crossing c
LEFT JOIN port p ON p.id = c.to_port
WHERE "port_code" IS NULL;
