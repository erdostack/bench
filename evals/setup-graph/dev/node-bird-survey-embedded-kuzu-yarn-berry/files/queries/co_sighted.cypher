// Species pairs seen at the same site on the same day, most often first.
MATCH (a:Species)-[x:SEEN_AT]->(s:Site)<-[y:SEEN_AT]-(b:Species)
WHERE a.code < b.code AND x.date = y.date
RETURN a.common_name AS species_a, b.common_name AS species_b, count(*) AS times
ORDER BY times DESC, species_a;
