// Games that share at least two mechanics with game 3, most overlap first.
MATCH (g:Game {id: 3})-[:HAS_MECHANIC]->(m:Mechanic)<-[:HAS_MECHANIC]-(other:Game)
WITH other, count(m) AS shared
WHERE shared >= 2
RETURN other.title AS game, shared
ORDER BY shared DESC, game;
