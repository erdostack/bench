// name: hand_over_cost_centres
MATCH (leaver:Employee {staff_no: $staff_no})-[:REPORTS_TO]->(mgr:Employee)
MATCH (leaver)-[o:OWNS]->(cc:CostCentre)
CREATE (mgr)-[:OWNS]->(cc)
DELETE o;

// name: remove_leaver
MATCH (e:Employee {staff_no: $staff_no})
DETACH DELETE e;
