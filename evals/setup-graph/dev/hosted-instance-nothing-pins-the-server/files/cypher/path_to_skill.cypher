MATCH p = (target:Skill {slug: 'tig-welding'})-[:BUILDS_ON*1..6]->(base:Skill)
WHERE NOT (base)-[:BUILDS_ON]->()
RETURN [s IN nodes(p) | s.slug] AS path
ORDER BY size(path);
