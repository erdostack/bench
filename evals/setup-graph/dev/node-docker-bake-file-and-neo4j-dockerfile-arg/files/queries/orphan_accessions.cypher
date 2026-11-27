MATCH (a:Accession)
WHERE NOT (a)-[:OF]->(:Variety)
RETURN a.code, a.year;
