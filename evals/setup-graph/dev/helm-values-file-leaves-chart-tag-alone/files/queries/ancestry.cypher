// Every ancestor of $name, with the number of generations back.
MATCH path = (v:Variety {name: $name})-[:BRED_FROM*1..12]->(a:Variety)
RETURN a.name AS ancestor, min(length(path)) AS generations
ORDER BY generations, ancestor;
