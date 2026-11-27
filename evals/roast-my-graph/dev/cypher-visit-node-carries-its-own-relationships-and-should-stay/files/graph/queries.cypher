// name: client_animals
MATCH (c:Client {id: $client_id})-[:OWNS]->(a:Animal)
RETURN a.id AS id, a.name AS name, a.species AS species
ORDER BY a.name;

// name: animal_record
MATCH (a:Animal {id: $animal_id})-[:HAD]->(v:Visit)-[:SEEN_BY]->(vet:Vet)
RETURN v.id AS visit, v.day AS day, v.reason AS reason, vet.name AS vet
ORDER BY v.day DESC
LIMIT 50;

// name: visit_detail
MATCH (a:Animal)-[:HAD]->(v:Visit {id: $visit_id})-[:SEEN_BY]->(vet:Vet)
RETURN a.name AS animal, v.day AS day, v.reason AS reason, v.notes AS notes, v.weight_kg AS weight_kg,
       vet.name AS vet;

// name: visit_prescriptions
MATCH (v:Visit {id: $visit_id})-[p:PRESCRIBED]->(d:Drug)
RETURN d.code AS code, d.name AS drug, p.dose AS dose, p.days AS days
ORDER BY d.name;

// name: earlier_visits
// The visits this one follows up on, nearest first.
MATCH path = (v:Visit {id: $visit_id})-[:FOLLOW_UP_OF*1..10]->(earlier:Visit)
RETURN earlier.id AS visit, earlier.day AS day, earlier.reason AS reason, length(path) AS steps_back
ORDER BY steps_back;

// name: day_sheet
MATCH (v:Visit {day: $day})-[:SEEN_BY]->(vet:Vet {id: $vet_id})
MATCH (a:Animal)-[:HAD]->(v)
RETURN v.slot AS slot, a.name AS animal, a.species AS species, v.reason AS reason
ORDER BY v.slot;

// name: drug_recall
MATCH (d:Drug {code: $drug_code})<-[:PRESCRIBED]-(v:Visit)<-[:HAD]-(a:Animal)<-[:OWNS]-(c:Client)
WHERE v.day >= $since
RETURN DISTINCT c.id AS client, c.phone AS phone, a.name AS animal, v.day AS day
ORDER BY day;
