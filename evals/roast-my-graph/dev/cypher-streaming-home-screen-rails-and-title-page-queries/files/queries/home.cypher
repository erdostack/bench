// name: continue_watching
MATCH (u:Viewer {id: $viewer})-[w:WATCHED]->(m:Title)
WHERE w.finished = false
RETURN m.id AS id, m.name AS name, w.position_s AS resume_at
ORDER BY w.at DESC
LIMIT 10;

// name: watch_next
MATCH (u:Viewer {id: $viewer})-[:FAVOURS]->(g:Genre),
      (m:Title)-[:IN_GENRE]->(:Genre)
WHERE m.available = true AND NOT (u)-[:WATCHED]->(m)
RETURN m.id AS id, m.name AS name, m.score AS score
ORDER BY m.score DESC
LIMIT 20;

// name: genre_rail
MATCH (m:Title)-[:IN_GENRE]->(g:Genre {code: $genre})
WHERE m.available = true
RETURN m.id AS id, m.name AS name, m.score AS score
ORDER BY m.score DESC
LIMIT 40;
