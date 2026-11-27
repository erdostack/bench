// 0007: delete pings from before 2026-09-01 with their FROM/NEAR; buses and stops stay. Count first: MATCH (p:Ping) WHERE p.at < datetime('2026-09-01T00:00:00Z') RETURN count(p)
MATCH (p:Ping) WHERE p.at < datetime('2026-09-01T00:00:00Z')
WITH collect(p) AS ps UNWIND ps AS x
CALL (x) { DETACH DELETE x } IN TRANSACTIONS OF 600 ROWS;
