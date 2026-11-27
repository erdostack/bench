// Three-tune runs where each change has been played at least twice.
MATCH (a:Tune)-[x:FOLLOWS]->(b:Tune)-[y:FOLLOWS]->(c:Tune)
WHERE x.times >= 2 AND y.times >= 2 AND a.id <> c.id
RETURN a.name AS first, b.name AS second, c.name AS third, x.times + y.times AS weight
ORDER BY weight DESC, first
LIMIT 15;
