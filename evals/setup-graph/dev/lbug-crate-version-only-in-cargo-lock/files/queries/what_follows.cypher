// What gets played straight after The Silver Spear, most common first.
MATCH (t:Tune {name: 'The Silver Spear'})-[f:FOLLOWS]->(next:Tune)
RETURN next.name AS tune, next.kind AS kind, f.times AS times
ORDER BY times DESC, tune;
