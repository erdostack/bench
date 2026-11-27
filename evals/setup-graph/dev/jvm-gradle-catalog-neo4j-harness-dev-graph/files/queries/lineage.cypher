// Trace a lot back to the garden its line was first saved in.
MATCH path = (lot:Lot {id: $lot})-[:GROWN_FROM*0..]->(origin:Lot)
WHERE NOT (origin)-[:GROWN_FROM]->()
MATCH (origin)-[:SAVED_AT]->(lib:Library)
RETURN [n IN nodes(path) | n.id] AS line, lib.name AS first_saved_at
