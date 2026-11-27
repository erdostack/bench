// Round trips of exactly $days stages that start and end at $start and never reuse a section.
MATCH path = (start:Hut {code: $start})-[:SECTION*2..5]-(start)
WHERE length(path) = $days
  AND all(s IN relationships(path) WHERE s.status = 'open')
RETURN [h IN nodes(path) | h.code] AS stages,
       reduce(total = 0, s IN relationships(path) | total + s.minutes) AS minutes
ORDER BY minutes
LIMIT 20
