// Substations fed by exactly one pipe: a single point of failure.
MATCH (s:Node {kind: 'substation'})<-[r:PIPE]-()
WITH s, count(r) AS feeds WHERE feeds = 1
RETURN s.code ORDER BY s.code;
