// name: team_header
MATCH (t:Team {id: $team})
RETURN t.name AS name, t.slack_channel AS channel, t.escalation_email AS escalation;

// name: on_call_now
MATCH (p:Person)-[s:ON_CALL]->(t:Team {id: $team})
WHERE s.start <= datetime() AND s.end > datetime()
RETURN p.name AS name, p.phone AS phone, s.end AS until;

// name: open_incidents
MATCH (i:Incident)-[:ASSIGNED_TO]->(t:Team {id: $team})
WHERE i.closed_at IS NULL
RETURN i.id AS id, i.title AS title, i.severity AS severity, i.opened_at AS opened
ORDER BY i.opened_at DESC
LIMIT 50;

// name: team_health
MATCH (p:Person)-[:MEMBER_OF]->(t:Team {id: $team})
MATCH (i:Incident)-[:ASSIGNED_TO]->(owner:Team {id: $team})
WHERE i.opened_at >= datetime() - duration('P90D')
RETURN count(p) AS members,
       count(i) AS incidents_90d,
       count(CASE WHEN i.severity = 'sev1' THEN 1 END) AS sev1_90d;
