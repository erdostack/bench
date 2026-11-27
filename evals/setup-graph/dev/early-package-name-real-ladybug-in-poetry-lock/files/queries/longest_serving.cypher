// Musicians by number of bands played in.
MATCH (m:Musician)-[:PLAYED_IN]->(b:Band)
RETURN m.name AS musician, count(b) AS bands
ORDER BY bands DESC, musician
LIMIT 10
