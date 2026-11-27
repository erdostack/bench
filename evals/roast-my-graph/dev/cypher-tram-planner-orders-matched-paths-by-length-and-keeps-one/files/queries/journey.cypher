// Fewest stops from $from to $to, for the journey search.
MATCH p = (a:Stop {id: $from})-[:LINK*]-(b:Stop {id: $to})
RETURN [s IN nodes(p) | s.name] AS stops, length(p) AS hops
ORDER BY hops
LIMIT 1;
