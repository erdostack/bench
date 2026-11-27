// BROADER chains that loop back on themselves (should never happen).
MATCH p = (t:Term)-[:BROADER*1..10]->(t)
RETURN [n IN nodes(p) | n.label] AS loop
LIMIT 20;
