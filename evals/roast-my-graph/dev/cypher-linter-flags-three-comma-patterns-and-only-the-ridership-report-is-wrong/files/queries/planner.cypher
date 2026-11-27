// name: same_line
MATCH (a:Station {code: $from}), (b:Station {code: $to})
MATCH (a)-[:ON]->(l:Line)<-[:ON]-(b)
RETURN l.code AS line, l.colour AS colour;

// name: station_board
MATCH (s:Station {code: $station})-[n:NEXT]->(following:Station)
RETURN n.line AS line, following.name AS next_stop, n.minutes AS minutes
ORDER BY n.line;

// name: zone_pairs
MATCH (z1:Zone), (z2:Zone)
WHERE z1.number <= z2.number
RETURN z1.number AS from_zone, z2.number AS to_zone
ORDER BY from_zone, to_zone;

// name: stations_in_zone
MATCH (z:Zone {number: $zone})<-[:IN_ZONE]-(s:Station)
RETURN s.code AS code, s.name AS name
ORDER BY s.name;
