// Species that lose every prey if $species disappears.
MATCH (gone:Species {id: $species})<-[:EATS]-(pred:Species)
WHERE NOT EXISTS { MATCH (pred)-[:EATS]->(other:Species) WHERE other <> gone }
RETURN pred.name AS at_risk;
