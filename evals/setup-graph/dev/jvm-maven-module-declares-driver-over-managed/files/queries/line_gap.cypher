// Fewest transfers between two lines, walking links included.
MATCH (a:Line {name: $from}), (b:Line {name: $to})
MATCH p = shortestPath((a)-[:CALLS_AT|WALK*..8]-(b))
RETURN [n IN nodes(p) | coalesce(n.name, n.code)] AS route;
