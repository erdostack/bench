MATCH (p:Patch)
WHERE NOT EXISTS { MATCH (p)-[:CORRIDOR]-(:Patch) }
RETURN p.id, p.hectares ORDER BY p.hectares DESC;
