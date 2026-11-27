// Huts reachable from $start within $budget minutes over open sections, nearest first.
MATCH path = (start:Hut {code: $start})-[:SECTION*1..6]-(hut:Hut)
WHERE hut <> start
  AND all(s IN relationships(path) WHERE s.status = 'open')
WITH hut, min(reduce(total = 0, s IN relationships(path) | total + s.minutes)) AS minutes
WHERE minutes <= $budget
RETURN hut.code AS hut, hut.name AS name, minutes
ORDER BY minutes, hut
