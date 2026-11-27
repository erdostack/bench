// Fewest-sailing route between P001 and P014.
MATCH p = shortestPath((a:Port {code: 'P001'})-[:SAILS_TO*..8]->(b:Port {code: 'P014'}))
RETURN [n IN nodes(p) | n.code] AS ports, reduce(t = 0, r IN relationships(p) | t + r.minutes) AS minutes;
