// Stations on the forecasters' map: everything still labelled Station, with its region.
MATCH (s:Station)-[:IN_REGION]->(r:Region)
RETURN s.code AS code, s.name AS name, s.status AS status, r.code AS region
ORDER BY code;
