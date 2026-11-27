// Everything $figure is computed from: jobs and datasets, nearest first.
MATCH path = (f:Figure {key: $figure})<-[:PRODUCES|READS*1..12]-(source)
RETURN labels(source)[0] AS kind, source.name AS name, length(path) AS distance
ORDER BY distance, name
