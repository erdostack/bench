// Every reach downstream of a spill point, with distance in reaches.
MATCH p = (:Reach {id: $reach})-[:FLOWS_INTO*1..40]->(down:Reach)
RETURN {reach: down.id, hops: length(p)} AS row
ORDER BY row.hops;
