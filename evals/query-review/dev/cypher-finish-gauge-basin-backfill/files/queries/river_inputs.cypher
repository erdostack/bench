MATCH (g:Gauge {basinCode: $basin})
RETURN g.gaugeId AS gaugeId, g.kind AS kind;
