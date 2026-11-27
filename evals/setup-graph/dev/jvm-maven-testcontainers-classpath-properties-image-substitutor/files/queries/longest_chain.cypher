MATCH p = (:Depot)-[:HANDED_TO*]->(:Clinic)
RETURN [n IN nodes(p) | n.name] AS chain, length(p) AS hops
ORDER BY hops DESC LIMIT 3
