MATCH (r:Reach) WHERE NOT ()-[:FLOWS_INTO]->(r)
RETURN r.id AS headwater ORDER BY headwater;
