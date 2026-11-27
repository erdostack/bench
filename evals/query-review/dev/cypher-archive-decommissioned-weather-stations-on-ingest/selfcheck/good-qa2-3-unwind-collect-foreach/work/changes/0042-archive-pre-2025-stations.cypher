// archive stations decommissioned before 2025 (they stay on the map otherwise); count: MATCH (s:Station {status: 'decommissioned'}) WHERE s.decommissionedOn < date('2025-01-01') RETURN count(s);
UNWIND ['decommissioned'] AS st
MATCH (s:Station {status: st}) WHERE s.decommissionedOn.year < 2025
WITH collect(s) AS ss
FOREACH (x IN ss | SET x:ArchivedStation REMOVE x:Station);
