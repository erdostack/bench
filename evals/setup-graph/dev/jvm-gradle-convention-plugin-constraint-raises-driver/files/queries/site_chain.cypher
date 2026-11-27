MATCH p = (a:Site {name: $from})-[:NEXT_STOP*1..5]->(b:Site {name: $to})
RETURN [n IN nodes(p) | n.name] AS chain LIMIT 10;
