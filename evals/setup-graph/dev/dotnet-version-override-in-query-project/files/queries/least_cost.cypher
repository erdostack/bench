MATCH (a:Patch {id: $from}), (b:Patch {id: $to})
MATCH p = shortestPath((a)-[:CORRIDOR*..10]-(b))
RETURN [n IN nodes(p) | n.id] AS route, reduce(c = 0.0, r IN relationships(p) | c + r.cost) AS cost;
