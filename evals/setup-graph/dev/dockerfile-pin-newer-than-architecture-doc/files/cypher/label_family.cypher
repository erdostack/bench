// A label together with its imprints, to any depth the shop has ever seen.
MATCH (parent:Label {name: 'Harbour Lights'})<-[:IMPRINT_OF*0..5]-(l:Label)
RETURN l.name AS label, count { (l)<-[:ON_LABEL]-(:Pressing) } AS pressings
ORDER BY pressings DESC;
