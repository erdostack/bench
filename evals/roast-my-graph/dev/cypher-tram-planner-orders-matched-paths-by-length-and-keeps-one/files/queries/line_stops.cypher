// The stops of one line in order.
MATCH (s:Stop)-[r:ON_LINE]->(:Line {code: $line})
RETURN s.id AS id, s.name AS name, r.seq AS seq
ORDER BY seq;
