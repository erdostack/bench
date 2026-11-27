// Gauges that measure water passing through a reach.
MATCH (:Reach {id: $reach})-[:FLOWS_INTO*0..40]->(:Reach)<-[:MEASURES]-(g:Gauge)
RETURN DISTINCT {gauge: g.id, river: g.river} AS row;
