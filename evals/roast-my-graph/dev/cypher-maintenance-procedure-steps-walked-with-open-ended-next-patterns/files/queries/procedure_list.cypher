// Latest version of every procedure, for the tablet's index.
MATCH (p:Procedure)
WITH p.id AS id, max(p.version) AS version
MATCH (p:Procedure {id: id, version: version})
RETURN p.id AS id, p.version AS version, p.title AS title
ORDER BY title;
