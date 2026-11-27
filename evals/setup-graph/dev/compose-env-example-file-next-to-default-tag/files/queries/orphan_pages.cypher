// Pages nothing links to.
MATCH (p:Page) WHERE NOT (p)<-[:LINKS_TO]-()
RETURN p.title AS page ORDER BY page;
