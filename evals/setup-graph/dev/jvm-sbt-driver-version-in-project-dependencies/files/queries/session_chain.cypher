MATCH p = (a:Musician {name: $from})-[:PLAYED_ON*..6]-(b:Musician {name: $to})
RETURN [n IN nodes(p) | coalesce(n.name, n.title)] AS chain
LIMIT 1;
