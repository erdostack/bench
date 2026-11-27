// 0007: delete pings from before 2026-09-01 with their FROM/NEAR; buses and stops stay. Count first: MATCH (p:Ping) WHERE p.at < datetime('2026-09-01T00:00:00Z') RETURN count(p)
MATCH (p:Ping) WHERE p.at < datetime('2026-09-01T00:00:00Z')
CALL (p) { OPTIONAL MATCH (p)-[r]-() WITH p, collect(r) AS rs FOREACH (x IN rs | DELETE x) DELETE p } IN TRANSACTIONS OF 600 ROWS;
