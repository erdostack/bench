// archive stations decommissioned before 2025 (they stay on the map otherwise); count: MATCH (s:Station {status: 'decommissioned'}) WHERE s.decommissionedOn < date('2025-01-01') RETURN count(s);
MATCH (s:Station {status: 'decommissioned'}) WHERE s.decommissionedOn < date('2025-01-01')
SET s:ArchivedStation;
