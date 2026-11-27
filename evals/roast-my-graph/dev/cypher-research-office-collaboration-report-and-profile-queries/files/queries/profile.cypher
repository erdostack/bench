// name: coauthors
MATCH (r:Researcher {id: $id})-[c:COAUTHORED]-(o:Researcher)
RETURN o.id AS id, o.name AS name, o.institute AS institute, c.papers AS papers
ORDER BY papers DESC, name;
