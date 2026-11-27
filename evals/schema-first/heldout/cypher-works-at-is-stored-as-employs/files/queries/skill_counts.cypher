MATCH (s:Skill)<-[:HAS_SKILL]-(p:Person)
RETURN s.name AS skill, count(p) AS people
ORDER BY people DESC;
