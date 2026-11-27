MATCH path = (a:Paper {doi: $from})-[:CITES*1..4]->(b:Paper {doi: $to})
RETURN [n IN nodes(path) | n.title] AS chain LIMIT 5;
