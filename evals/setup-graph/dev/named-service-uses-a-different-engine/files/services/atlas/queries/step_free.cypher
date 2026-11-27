// Junctions that can be reached from the station forecourt without using a stepped segment.
MATCH (a:Junction {ref: 'J001'})-[e:PATH*1..30 (r, n | WHERE NOT r.steps)]-(b:Junction)
RETURN DISTINCT b.ref AS junction, b.ward AS ward
ORDER BY junction;
