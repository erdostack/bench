downstream_meters suffers from path-binding cardinality blow-up before its DISTINCT. Push DISTINCT down, add a LIMIT and an index hint. One high finding; see docs/graph/ROAST.md and findings.json.
