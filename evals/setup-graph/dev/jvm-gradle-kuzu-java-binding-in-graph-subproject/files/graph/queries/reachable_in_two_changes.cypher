MATCH (a:Stop {code: $stop})-[:TRANSFER*1..2]->(b:Stop)
RETURN DISTINCT b.code, b.name
ORDER BY b.code;
