// Pairs of sets that have a tune in common.
MATCH (a:TuneSet)<-[:IN_SET]-(t:Tune)-[:IN_SET]->(b:TuneSet)
WHERE a.id < b.id
RETURN a.name AS first_set, b.name AS second_set, collect(t.name) AS shared
ORDER BY first_set, second_set;
