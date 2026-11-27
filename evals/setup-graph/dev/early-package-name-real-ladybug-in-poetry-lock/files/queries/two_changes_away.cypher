// Bands exactly two line-up hops from $band (a member of a band that shares a member with it).
MATCH (b:Band {name: $band})<-[:PLAYED_IN]-(:Musician)-[:PLAYED_IN]->(mid:Band)<-[:PLAYED_IN]-(:Musician)-[:PLAYED_IN]->(far:Band)
WHERE far.id <> b.id AND mid.id <> b.id AND far.id <> mid.id
  AND NOT EXISTS { MATCH (b)<-[:PLAYED_IN]-(:Musician)-[:PLAYED_IN]->(far) }
RETURN DISTINCT far.name AS band, mid.name AS via
ORDER BY band, via
