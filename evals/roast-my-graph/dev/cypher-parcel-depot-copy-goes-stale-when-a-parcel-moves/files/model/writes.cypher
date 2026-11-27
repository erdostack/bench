// name: register_parcel
MATCH (d:Depot {code: $depot})
CREATE (p:Parcel {tracking_no: $tracking_no, weight_g: $weight_g, status: 'waiting',
                  depot_code: d.code, registered_at: datetime()})
CREATE (p)-[:AT {since: datetime()}]->(d);

// name: move_parcel
MATCH (p:Parcel {tracking_no: $tracking_no})-[here:AT]->(:Depot)
MATCH (next:Depot {code: $to_depot})
DELETE here
CREATE (p)-[:AT {since: datetime()}]->(next)
SET p.status = 'waiting';

// name: load_on_route
MATCH (p:Parcel {tracking_no: $tracking_no})
MATCH (r:Route {id: $route_id})
MERGE (p)-[:LOADED_ON]->(r)
SET p.status = 'out_for_delivery';

// name: mark_in_transit
MATCH (p:Parcel {tracking_no: $tracking_no})
SET p.status = 'in_transit';

// name: mark_delivered
MATCH (p:Parcel {tracking_no: $tracking_no})
SET p.status = 'delivered', p.delivered_at = datetime();
