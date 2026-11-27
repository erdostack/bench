// What could stand in for buttermilk, allowing a swap of a swap?
MATCH (a:Ingredient {name: 'buttermilk'})<-[:SWAPS_FOR*1..2]-(b:Ingredient)
RETURN DISTINCT b.name AS stand_in;
