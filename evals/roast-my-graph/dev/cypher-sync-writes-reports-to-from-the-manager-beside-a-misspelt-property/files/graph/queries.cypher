// name: chain_of_command
MATCH path = (e:Employee {staff_no: $staff_no})-[:REPORTS_TO*1..9]->(boss:Employee)
RETURN boss.staff_no AS staff_no, boss.full_name AS full_name, length(path) AS levels_up
ORDER BY levels_up;

// name: approver_for
MATCH path = (e:Employee {staff_no: $staff_no})-[:REPORTS_TO*1..9]->(boss:Employee)
WHERE boss.active AND boss.managment_level <= $max_level
RETURN boss.staff_no AS approver
ORDER BY length(path)
LIMIT 1;

// name: direct_reports
MATCH (boss:Employee {staff_no: $staff_no})<-[:REPORTS_TO]-(e:Employee)
WHERE e.active
RETURN e.staff_no AS staff_no, e.full_name AS full_name
ORDER BY e.full_name;

// name: headcount_under
MATCH (boss:Employee {staff_no: $staff_no})<-[:REPORTS_TO*1..9]-(e:Employee)
WHERE e.active
RETURN count(DISTINCT e) AS headcount;

// name: team_roster
MATCH (t:Team {code: $team})<-[:IN_TEAM]-(e:Employee)
WHERE e.active
OPTIONAL MATCH (e)-[:BASED_AT]->(s:Site)
RETURN e.staff_no AS staff_no, e.full_name AS full_name, s.city AS city
ORDER BY e.full_name;
