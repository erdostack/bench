MATCH (a:Branch)-[l:LENT_TO]->(b:Branch)
RETURN a.name, b.name, count(*) AS loans, sum(l.items) AS items
ORDER BY items DESC
LIMIT 10;
