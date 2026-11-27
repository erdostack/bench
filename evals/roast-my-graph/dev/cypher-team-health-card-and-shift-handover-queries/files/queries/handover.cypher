// name: hand_over_shift
MATCH (from:Person {id: $from}), (to:Person {id: $to})
MATCH (from)-[s:ON_CALL]->(t:Team {id: $team})
WHERE s.start <= datetime() AND s.end > datetime()
CREATE (to)-[:ON_CALL {start: datetime(), end: s.end, handed_from: from.id}]->(t)
SET s.end = datetime();
