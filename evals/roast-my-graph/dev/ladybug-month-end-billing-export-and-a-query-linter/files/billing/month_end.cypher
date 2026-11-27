MATCH (c:Customer)-[:OWNS]->(m:Meter)-[:RECORDED]->(r:Reading)
WHERE r.month = $month
RETURN c.id AS customer, c.tariff AS tariff, m.serial AS meter, r.kwh AS kwh
ORDER BY customer, meter;
