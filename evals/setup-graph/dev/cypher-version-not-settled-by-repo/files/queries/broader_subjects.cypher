// Subjects above $subject in the hierarchy, nearest first.
MATCH path = (s:Subject {label: $subject})-[:BROADER*1..10]->(up:Subject)
RETURN up.label AS subject, length(path) AS steps
ORDER BY steps
