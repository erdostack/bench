// The steps of one procedure version, in order.
MATCH (:Procedure {id: $id, version: $version})-[:FIRST]->(first:Step)
MATCH (first)-[:NEXT*0..]->(s:Step)
RETURN s.n AS n, s.text AS text
ORDER BY n;
