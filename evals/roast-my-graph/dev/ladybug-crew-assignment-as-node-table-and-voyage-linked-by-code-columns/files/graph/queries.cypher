// name: current_crew
MATCH (s:Sailor)-[:HasAssignment]->(a:CrewAssignment)-[:AssignmentOn]->(v:Vessel)
WHERE v.imo = $imo AND a.signed_off IS NULL
RETURN s.full_name, a.role, a.signed_on
ORDER BY a.signed_on;

// name: service_record
MATCH (s:Sailor)-[:HasAssignment]->(a:CrewAssignment)-[:AssignmentOn]->(v:Vessel)
WHERE s.id = $sailor_id
RETURN v.name, a.role, a.signed_on, a.signed_off
ORDER BY a.signed_on;

// name: departures_from_port
MATCH (y:Voyage), (p:Port)
WHERE p.code = $code AND y.origin_port_code = p.code
RETURN y.id, y.vessel_imo, y.departed, p.name
ORDER BY y.departed DESC
LIMIT 100;

// name: ports_served_by_vessel
MATCH (y:Voyage), (p:Port)
WHERE y.vessel_imo = $imo AND (p.code = y.origin_port_code OR p.code = y.dest_port_code)
RETURN DISTINCT p.code, p.name;
