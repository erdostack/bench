// Fewest clicks from $from to $to.
MATCH path = shortestPath((a:Page {title: $from})-[:LINKS_TO*..10]->(b:Page {title: $to}))
RETURN [n IN nodes(path) | n.title] AS pages;
