// 0007: delete pings from before 2026-09-01 with their FROM/NEAR; buses and stops stay. Count first: MATCH (p:Ping) WHERE p.at < datetime('2026-09-01T00:00:00Z') RETURN count(p)
CALL apoc.periodic.iterate('MATCH (p:Ping) WHERE p.at < $cut RETURN p', 'DETACH DELETE p', {batchSize: 600, params: {cut: datetime('2026-09-01T00:00:00Z')}});
