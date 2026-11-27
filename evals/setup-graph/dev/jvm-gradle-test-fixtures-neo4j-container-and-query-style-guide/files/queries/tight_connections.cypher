MATCH (a:Leg)-[c:CONNECTS]->(b:Leg)
WHERE c.minutes < 45
RETURN a.flight, b.flight, c.minutes
ORDER BY c.minutes
