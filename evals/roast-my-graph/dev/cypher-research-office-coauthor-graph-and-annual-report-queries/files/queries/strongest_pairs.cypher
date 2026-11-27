MATCH (a:Researcher)-[c:COAUTHORED]->(b:Researcher)
RETURN a.name, b.name, c.papers
ORDER BY c.papers DESC
LIMIT 20;
