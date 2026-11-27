// Buildings fed from substation SS-14, with the pipe length on the way.
MATCH p = (:Node {code: 'SS-14'})-[:PIPE*1..8]->(b:Node {kind: 'building'})
RETURN b.code AS building, reduce(m = 0, r IN relationships(p) | m + r.length_m) AS metres
ORDER BY metres;
