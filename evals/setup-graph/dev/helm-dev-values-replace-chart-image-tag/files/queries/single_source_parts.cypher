// Parts with exactly one supplier that are used in more than one assembly.
MATCH (s:Supplier)-[:SUPPLIES]->(p:Part)
WITH p, collect(s.name) AS suppliers
WHERE size(suppliers) = 1
MATCH (a:Assembly)-[:CONTAINS*1..8]->(p)
WITH p, suppliers, count(DISTINCT a) AS assemblies
WHERE assemblies > 1
RETURN p.sku AS part, suppliers[0] AS supplier, assemblies
ORDER BY assemblies DESC, part
