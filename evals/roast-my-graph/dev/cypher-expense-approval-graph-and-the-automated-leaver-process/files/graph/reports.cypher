// name: audit_trail
MATCH (c:Claim {ref: $ref})
OPTIONAL MATCH (s:Employee)-[:SUBMITTED]->(c)
OPTIONAL MATCH (a:Employee)-[ap:APPROVED]->(c)
RETURN c.ref AS claim, c.amount AS amount, s.name AS submitted_by, a.name AS approved_by, ap.at AS approved_at;

// name: spend_by_cost_centre
MATCH (cc:CostCentre)<-[:OWNS]-(owner:Employee)
MATCH (owner)<-[:REPORTS_TO*0..]-(:Employee)-[:SUBMITTED]->(c:Claim {status: 'paid'})
RETURN cc.code AS cost_center, sum(c.amount) AS spend
ORDER BY spend DESC;
