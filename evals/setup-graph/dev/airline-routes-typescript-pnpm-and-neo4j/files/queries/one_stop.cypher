MATCH (a:Airport {iata: $from})-[r1:ROUTE]->(hub:Airport)-[r2:ROUTE]->(b:Airport {iata: $to})
WHERE hub <> a AND hub <> b
RETURN hub.iata AS via, r1.carrier AS first, r2.carrier AS second
ORDER BY via;
