MATCH (r:Recipe)-[:USES]->(:Ingredient {name: 'buttermilk'})
RETURN r.title
