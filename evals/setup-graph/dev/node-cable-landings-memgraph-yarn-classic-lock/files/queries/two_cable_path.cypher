// Countries reachable from $from using at most two cables.
MATCH (:Country {iso: $from})<-[:IN]-(:Station)<-[:LANDS_AT]-(c1:Cable)-[:LANDS_AT]->(:Station)-[:IN]->(mid:Country)
OPTIONAL MATCH (mid)<-[:IN]-(:Station)<-[:LANDS_AT]-(c2:Cable)-[:LANDS_AT]->(:Station)-[:IN]->(far:Country)
RETURN DISTINCT coalesce(far.iso, mid.iso) AS country
ORDER BY country;
