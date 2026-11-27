// Fewest board seats between two companies.
MATCH (a:Company {id: $from}), (b:Company {id: $to})
MATCH p = shortestPath((a)-[:SITS_ON*..8]-(b))
RETURN length(p) / 2 AS directorsBetween, [n IN nodes(p) | coalesce(n.name, n.id)] AS chain;
