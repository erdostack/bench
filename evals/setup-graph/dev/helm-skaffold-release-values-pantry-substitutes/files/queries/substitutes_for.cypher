MATCH (i:Ingredient {name: 'buttermilk'})-[s:SUBSTITUTES_FOR]->(alt:Ingredient)
RETURN alt.name AS use_instead, s.ratio AS ratio
ORDER BY ratio;
