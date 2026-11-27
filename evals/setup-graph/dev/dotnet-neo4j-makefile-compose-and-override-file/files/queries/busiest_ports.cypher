// Ports with the most departures.
MATCH (p:Port)-[s:SAILS_TO]->()
RETURN p.code AS port, count(s) AS departures
ORDER BY departures DESC
LIMIT 10;
