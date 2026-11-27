MATCH (a:Person {login: $from}), (b:Person {login: $to})
MATCH p = shortestPath((a)-[:REVIEWED|TOUCHED*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.login, n.path)] AS path;
