// name: guide_page
MATCH (g:Guide {id: $id})<-[w:WROTE]-(a:Author)
RETURN g.title, g.difficulty, g.published, a.handle, w.at;

// name: guide_countries
MATCH (g:Guide {id: $id})-[:AVAILABLE_IN]->(c:Country)
RETURN c.iso, c.name
ORDER BY c.name;

// name: related_guides
MATCH (g:Guide {id: $id})-[:ABOUT]->(t:Topic)<-[:ABOUT]-(other:Guide)
WHERE other.id <> $id
RETURN other.id, other.title, count(t) AS shared
ORDER BY shared DESC, other.published DESC
LIMIT 5;

// name: topic_page
MATCH (t:Topic {slug: $slug})<-[:ABOUT]-(g:Guide)
WHERE t.slug <> 'general'
RETURN g.id, g.title, g.published
ORDER BY g.published DESC
LIMIT 50;
