// name: host_by_serial
MATCH (h:Host {serial: $serial})
RETURN h.name AS name, h.os AS os;

// name: services_on_host
MATCH (h:Host {name: $host})-[:RUNS_ON]->(s:Service)
RETURN s.name AS service, s.tier AS tier
ORDER BY s.tier;

// name: owners_to_page
MATCH (h:Host {name: $host})<-[:RUNS_ON]-(s:Service)<-[:OWNS]-(t:Team)
RETURN DISTINCT t.slug AS team, t.pager AS pager;

// name: upstream_of
MATCH (s:Service {name: $service})-[:DEPENDS_ON*1..4]->(dep:Service)
RETURN DISTINCT dep.name AS service, dep.tier AS tier;

// name: rack_inventory
MATCH (r:Rack {code: $rack})<-[:MOUNTED_IN]-(h:Host)
RETURN h.name AS host, h.os AS os
ORDER BY h.name;

// name: tier_one_services
MATCH (s:Service)
WHERE s.tier = 1
RETURN s.name AS service
ORDER BY s.name;
