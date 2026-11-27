// name: title_page
MATCH (m:Title {id: $title})
OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
RETURN m.name AS name, m.synopsis AS synopsis, m.score AS score, collect(g.name) AS genres;
