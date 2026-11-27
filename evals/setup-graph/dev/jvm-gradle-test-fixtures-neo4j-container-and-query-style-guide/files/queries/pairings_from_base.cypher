MATCH p = (first:Leg {origin: $base})-[:CONNECTS*1..4]->(last:Leg {destination: $base})
RETURN [l IN nodes(p) | l.flight] AS legs, length(p) + 1 AS duty_legs
ORDER BY duty_legs
