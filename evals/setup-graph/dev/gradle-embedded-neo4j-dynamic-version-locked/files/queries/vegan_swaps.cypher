// Fewest swaps that make recipe $recipe vegan.
MATCH (r:Recipe {slug: $recipe})-[:USES]->(i:Ingredient)
WHERE NOT i.vegan
OPTIONAL MATCH (i)-[:REPLACED_BY {diet: 'vegan'}]->(s:Ingredient)
RETURN i.name AS ingredient, collect(s.name) AS options
ORDER BY ingredient;
