// name: depot_backlog
MATCH (p:Parcel)
WHERE p.depot_code = $depot AND p.status = 'waiting'
RETURN p.tracking_no AS tracking_no, p.weight_g AS weight_g, p.registered_at AS registered_at
ORDER BY p.registered_at
LIMIT 200;

// name: parcel_trace
MATCH (p:Parcel {tracking_no: $tracking_no})-[here:AT]->(d:Depot)
OPTIONAL MATCH (p)-[:LOADED_ON]->(r:Route)
RETURN p.status AS status, d.code AS depot, d.city AS city, here.since AS since, r.id AS route;

// name: route_manifest
MATCH (r:Route {id: $route_id})<-[:LOADED_ON]-(p:Parcel)
RETURN p.tracking_no AS tracking_no, p.weight_g AS weight_g
ORDER BY p.tracking_no;

// name: depot_load
MATCH (d:Depot {code: $depot})<-[:AT]-(p:Parcel)
WHERE p.status = 'waiting'
RETURN count(p) AS parcels, sum(p.weight_g) AS grams;
