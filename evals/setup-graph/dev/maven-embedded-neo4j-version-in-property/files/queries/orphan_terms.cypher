// Terms with no broader term that are not a scheme's top term.
MATCH (t:Term)
WHERE NOT (t)-[:BROADER]->() AND NOT coalesce(t.top, false)
RETURN t.scheme AS scheme, t.label AS term
ORDER BY scheme, term;
