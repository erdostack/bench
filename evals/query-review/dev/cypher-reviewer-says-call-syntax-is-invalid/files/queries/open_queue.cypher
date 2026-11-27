// The desk's default queue.
// Parameters: $team, $limit
// Returns: id, subject, openedAt
MATCH (:Team {id: $team})<-[:ASSIGNED_TO]-(t:Ticket)
WHERE t.status = 'open' AND NOT t:Archived
RETURN t.id AS id, t.subject AS subject, t.openedAt AS openedAt
ORDER BY openedAt
LIMIT $limit;
