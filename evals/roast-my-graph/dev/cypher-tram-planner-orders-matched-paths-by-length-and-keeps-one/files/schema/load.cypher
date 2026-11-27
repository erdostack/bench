// Loaded from the network export; one row per pair of consecutive stops on a line.
LOAD CSV WITH HEADERS FROM 'file:///stops.csv' AS row
MERGE (s:Stop {id: row.stop_id})
SET s.name = row.name, s.zone = toInteger(row.zone);

LOAD CSV WITH HEADERS FROM 'file:///links.csv' AS row
MATCH (a:Stop {id: row.from_id}), (b:Stop {id: row.to_id})
MERGE (a)-[l:LINK]->(b)
SET l.minutes = toFloat(row.minutes);

LOAD CSV WITH HEADERS FROM 'file:///line_stops.csv' AS row
MERGE (l:Line {code: row.line})
WITH l, row
MATCH (s:Stop {id: row.stop_id})
MERGE (s)-[r:ON_LINE]->(l)
SET r.seq = toInteger(row.seq);
