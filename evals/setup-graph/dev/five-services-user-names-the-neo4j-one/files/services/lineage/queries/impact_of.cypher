// Report figures that change if $dataset changes.
MATCH (d:Dataset {name: $dataset})-[:READS|PRODUCES*1..12]->(f:Figure)
RETURN DISTINCT f.key AS figure, f.report AS report
ORDER BY report, figure
