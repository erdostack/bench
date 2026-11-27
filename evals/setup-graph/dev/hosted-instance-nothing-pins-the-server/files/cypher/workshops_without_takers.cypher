MATCH (w:Workshop)-[:TEACHES]->(s:Skill)
WHERE NOT EXISTS { (:Learner)-[:WANTS]->(s) }
RETURN w.title AS workshop, collect(s.slug) AS skills;
