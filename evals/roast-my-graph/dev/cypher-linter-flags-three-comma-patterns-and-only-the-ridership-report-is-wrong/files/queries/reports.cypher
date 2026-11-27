// name: busiest_stations
MATCH (t:Tap)-[:AT]->(s:Station)
WHERE t.day = $day
RETURN s.name AS station, count(t) AS taps
ORDER BY taps DESC
LIMIT 20;

// name: line_ridership
MATCH (t:Tap)
WHERE t.day >= $from AND t.day <= $to
MATCH (s:Station)-[:ON]->(l:Line {code: $line})
RETURN s.name AS station, count(t) AS taps
ORDER BY taps DESC;

// name: card_mix
MATCH (t:Tap)
WHERE t.day = $day
RETURN t.card_kind AS card_kind, count(t) AS taps
ORDER BY taps DESC;
