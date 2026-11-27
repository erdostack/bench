// Stops served by three or more routes.
MATCH (s:Stop)<-[:SERVES]-(r:Route)
WITH s, count(DISTINCT r) AS routes WHERE routes >= 3
RETURN s.name AS stop, routes ORDER BY routes DESC, stop;
