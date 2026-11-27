// name: sync_employees
UNWIND $rows AS row
MERGE (e:Employee {staff_no: row.staff_no})
SET e.full_name = row.full_name,
    e.managment_level = toInteger(row.level),
    e.active = (row.status = 'active');

// name: clear_lines
MATCH (:Employee)-[r:REPORTS_TO|IN_TEAM|BASED_AT]->()
DELETE r;

// name: sync_teams
UNWIND $rows AS row
MATCH (e:Employee {staff_no: row.staff_no})
MERGE (t:Team {code: row.team_code})
SET t.name = row.team_name
MERGE (e)-[:IN_TEAM]->(t);

// name: sync_sites
UNWIND $rows AS row
MATCH (e:Employee {staff_no: row.staff_no})
MERGE (s:Site {code: row.site_code})
SET s.city = row.site_city
MERGE (e)-[:BASED_AT]->(s);

// name: sync_reporting_lines
// one row per employee who has a line manager: staff_no, manager_staff_no
UNWIND $rows AS row
MATCH (e:Employee {staff_no: row.staff_no})
MATCH (m:Employee {staff_no: row.manager_staff_no})
MERGE (m)-[:REPORTS_TO]->(e);
