MATCH p = shortestPath((a:Exchange {name: $from})-[:CABLE*..12]-(b:Exchange {name: $to}))
RETURN reduce(m = 0, r IN relationships(p) | m + r.metres) AS metres;
