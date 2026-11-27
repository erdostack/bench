// Bands that share at least one musician with $band, and who the go-betweens are.
MATCH (b:Band {name: $band})<-[:PLAYED_IN]-(m:Musician)-[:PLAYED_IN]->(other:Band)
WHERE other.id <> b.id
RETURN other.name AS band, collect(m.name) AS shared
ORDER BY size(shared) DESC, band
