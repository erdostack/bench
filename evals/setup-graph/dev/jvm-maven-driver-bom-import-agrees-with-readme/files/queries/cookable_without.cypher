// Recipes that can still be made without $missing, using at most one substitution.
MATCH (r:Recipe)-[:NEEDS]->(m:Ingredient {name: $missing})
OPTIONAL MATCH (m)<-[s:SUBSTITUTES]-(alt:Ingredient)
WITH r, collect(alt.name) AS alternatives
WHERE size(alternatives) > 0
RETURN r.title AS recipe, alternatives ORDER BY recipe;
