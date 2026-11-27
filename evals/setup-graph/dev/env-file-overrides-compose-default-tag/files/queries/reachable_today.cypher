// Ports reachable from one port with at most three sailings, each caught after the previous one arrives.
MATCH path = (start:Port {code: coalesce($port, 'SKA')})
             ((a:Port)<-[:DEPARTS_FROM]-(s:Sailing)-[:ARRIVES_AT]->(b:Port)){1,3}(target:Port)
WHERE all(i IN range(0, size(s) - 2) WHERE s[i].arrives < s[i + 1].departs)
RETURN DISTINCT target.name AS port, size(s) AS sailings
ORDER BY sailings, port;
