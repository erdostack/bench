// name: track
MATCH (s:Shipment {id: $id})-[b:SHIPPED_BY]->(c:Carrier)
OPTIONAL MATCH (s)-[e:SCANNED_AT]->(d:Depot)
RETURN s.status AS status, c.name AS carrier, b.tracking_no AS tracking_no,
       e.at AS at, e.event AS event, d.city AS city
ORDER BY at;

// name: customer_shipments
MATCH (s:Shipment)-[:FOR_CUSTOMER]->(cu:Customer {id: $customer})
WHERE s.created >= $since
MATCH (s)-[b:SHIPPED_BY]->(c:Carrier)
RETURN s.id AS id, s.created AS created, s.status AS status, c.name AS carrier, b.service AS service
ORDER BY created DESC
LIMIT 100;
